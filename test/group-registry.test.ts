import assert from "node:assert/strict";
import { restoreHistoricalGroups, trackGroupUpdate } from "../src/tracking/groupRegistry.js";
import { setCustomFirestoreDb, resetFirestoreState } from "../src/firebase/firestore.js";

function fakeFirestore() {
  const collections = new Map<string, Map<string, any>>();
  let failCollection = "";
  const rows = (name: string) => {
    if (!collections.has(name)) collections.set(name, new Map());
    return collections.get(name)!;
  };
  const query = (name: string, after = "", limit = Infinity): any => ({
    select: () => query(name, after, limit),
    orderBy: () => query(name, after, limit),
    limit: (n: number) => query(name, after, n),
    startAfter: (id: string) => query(name, id, limit),
    get: async () => {
      if (failCollection === name) throw new Error("OFFLINE");
      return { docs: [...rows(name)].sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0)
        .filter(([id]) => id > after).slice(0, limit)
        .map(([id, data]) => ({ id, data: () => data })) };
    },
  });
  const db: any = {
    rows,
    fail: (name: string) => { failCollection = name; },
    collection: (name: string) => ({
      ...query(name),
      doc: (id: string) => ({
        get: async () => ({ exists: rows(name).has(id), data: () => rows(name).get(id) }),
        set: async (data: any, options?: any) => {
          rows(name).set(id, options?.merge ? { ...rows(name).get(id), ...data } : { ...data });
        },
      }),
    }),
    runTransaction: async (fn: any) => fn({
      get: (ref: any) => ref.get(),
      set: (ref: any, data: any, options?: any) => ref.set(data, options),
    }),
  };
  return db;
}

async function run() {
  const db = fakeFirestore();
  setCustomFirestoreDb(db);
  try {
    let nextCalls = 0;
    for (const type of ["group", "supergroup"]) {
      await trackGroupUpdate({ chat: { id: -10, type, title: "Quizsiz guruh" } } as any, async () => { nextCalls++; });
    }
    assert.equal(db.rows("groups").get("-10").title, "Quizsiz guruh");
    assert.equal(nextCalls, 2);
    for (const type of ["private", "channel"]) {
      await trackGroupUpdate({ chat: { id: 20, type, title: "Boshqa" } } as any, async () => {});
    }
    assert.equal(db.rows("groups").has("20"), false);
    db.rows("groups").set("-10", { ...db.rows("groups").get("-10"), status: "kicked" });
    await trackGroupUpdate({ chat: { id: -10, type: "group", title: "Eski tugma" } } as any, async () => {});
    assert.equal(db.rows("groups").get("-10").status, "kicked", "Oddiy hodisa botni qayta faol qilmasin");
    console.log("✅ Quizsiz guruh qayd etildi, private/channel o'tkazildi, chiqarilgan guruh holati saqlandi.");

    for (let i = 0; i < 205; i++) {
      db.rows("quiz_results").set(`row${String(i).padStart(3, "0")}`, {
        chatId: -1001, createdAt: new Date(Date.UTC(2025, 0, 1) + i * 1000).toISOString(),
      });
    }
    for (const id of [-1002, -1003, -1004, -1005, -1006, 1234]) {
      db.rows("quiz_sessions").set(String(id), { chatId: id, savedAt: Date.UTC(2025, 0, 1) });
    }
    const existing = { chatId: -1002, title: "Yangi nom", status: "kicked", memberCount: 17 };
    db.rows("groups").set("-1002", { ...existing });
    let requests = 0;
    const api: any = {
      getMe: async () => ({ id: 99 }),
      getChat: async (id: number) => {
        requests++;
        if (id === -1003) throw new Error("Network unavailable");
        if (id === -1004) return { id, type: "channel", title: "Kanal" };
        if (id === -1005) db.rows("groups").set(String(id), { status: "kicked", title: "Live event wins" });
        return { id, type: "supergroup", title: `Kimyo ${id}` };
      },
      getChatMember: async (id: number, botId: number) => {
        assert.equal(botId, 99);
        return { status: id === -1006 ? "left" : "administrator" };
      },
      getChatMemberCount: async () => 25,
    };
    const result = await restoreHistoricalGroups(api, db);
    assert.equal(result.discovered, 6);
    assert.equal(result.added, 3);
    assert.equal(result.unresolved, 1);
    assert.equal(db.rows("groups").get("-1001").title, "Kimyo -1001");
    assert.equal(db.rows("groups").get("-1001").lastActivity, "2025-01-01T00:03:24.000Z");
    assert.deepEqual(db.rows("groups").get("-1002"), existing);
    assert.equal(db.rows("groups").get("-1003").status, "unknown");
    assert.equal(db.rows("groups").has("-1004"), false);
    assert.equal(db.rows("groups").get("-1005").title, "Live event wins");
    assert.equal(db.rows("groups").get("-1006").status, "left");
    assert.equal(db.rows("groups").has("1234"), false);
    const previousRequests = requests;
    assert.equal((await restoreHistoricalGroups(api, db)).alreadyCompleted, true);
    assert.equal(requests, previousRequests);
    console.log("✅ 200+ eski yozuv sahifalandi, guruhlar takrorsiz tiklandi, joriy ma'lumotlar saqlandi.");

    const unavailable = fakeFirestore();
    unavailable.fail("quiz_results");
    await assert.rejects(restoreHistoricalGroups(api, unavailable), /OFFLINE/);
    assert.equal(unavailable.rows("admin_migrations").size, 0, "Xatoda tiklash yakunlangan deb belgilanmasin");
    unavailable.fail("");
    assert.equal((await restoreHistoricalGroups(api, unavailable)).alreadyCompleted, false);
    console.log("✅ Baza xatosi yashirilmadi; tiklashni keyin qayta boshlash mumkin.");
  } finally {
    resetFirestoreState();
  }
}

run().catch((error) => { console.error(error); process.exitCode = 1; });
