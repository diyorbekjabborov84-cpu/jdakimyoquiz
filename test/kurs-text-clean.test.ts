import assert from "node:assert";
import { cleanKursText, validateKursDarslarPayload } from "../src/kurs/kursRepository.js";

/**
 * Qo'llanma HTML'idan kelgan teglar Telegram poll matniga tushmasligi:
 * <sub>/<sup> → Unicode indeks, boshqa teglar olib tashlanadi, entity'lar ochiladi.
 */

assert.strictEqual(cleanKursText("Mis atomi (A<sub>r</sub> = 64)"), "Mis atomi (Aᵣ = 64)");
assert.strictEqual(cleanKursText("H<sub>2</sub>SO<sub>4</sub>"), "H₂SO₄");
assert.strictEqual(cleanKursText("Ca(OH)<sub>2</sub>"), "Ca(OH)₂");
assert.strictEqual(cleanKursText("1,67·10<sup>-24</sup> g"), "1,67·10⁻²⁴ g");
assert.strictEqual(cleanKursText("M<sub>r</sub>"), "Mᵣ");
// Unicode'da yo'q harf o'zgarishsiz qoladi
assert.strictEqual(cleanKursText("X<sub>q</sub>"), "Xq");
assert.strictEqual(cleanKursText("<b>Qalin</b> va <i>yotiq</i>"), "Qalin va yotiq");
assert.strictEqual(cleanKursText("A &amp; B &lt; C &#8594; D"), "A & B < C → D");
assert.strictEqual(cleanKursText("Bir<br/>ikki"), "Bir ikki");
assert.strictEqual(cleanKursText("  oddiy matn  "), "oddiy matn");
// Teg bo'lmagan "<" belgisi saqlanadi
assert.strictEqual(cleanKursText("p < e emas"), "p < e emas");

const res = validateKursDarslarPayload([
  {
    dars: 99,
    mavzu: "Sinov M<sub>r</sub>",
    testlar: [
      {
        id: "d99_t01",
        savol: "CO<sub>2</sub> ning M<sub>r</sub> qiymati?",
        variantlar: { A: "28", B: "44", C: "H<sub>2</sub>O", D: "<b>16</b>" },
        javob: "B",
      },
    ],
    mashqlar: ["NH<sub>3</sub> ni o'qing", { id: "x", savol: "O<sub>3</sub>", yechim: "ozon<br>" }],
  },
]);
assert.ok(res.valid, res.errors.join("; "));
const d = res.validated[0];
assert.strictEqual(d.mavzu, "Sinov Mᵣ");
assert.strictEqual(d.testlar[0].savol, "CO₂ ning Mᵣ qiymati?");
assert.deepStrictEqual(d.testlar[0].variantlar, { A: "28", B: "44", C: "H₂O", D: "16" });
assert.strictEqual(d.mashqlar?.[0].savol, "NH₃ ni o'qing");
assert.strictEqual(d.mashqlar?.[1].savol, "O₃");
assert.strictEqual(d.mashqlar?.[1].yechim, "ozon");

console.log("✅ Kurs matnini HTML teglardan tozalash testlari o'tdi");
