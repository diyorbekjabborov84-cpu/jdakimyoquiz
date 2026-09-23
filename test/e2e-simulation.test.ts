import assert from "node:assert";
import { sampleChemistryQuiz } from "../src/quiz/questions.js";
import { QuizManager, TelegramApiSender } from "../src/quiz/quizManager.js";

class E2ETestApi implements TelegramApiSender {
  public messages: string[] = [];
  public polls: Array<{
    pollId: string;
    messageId: number;
    question: string;
    options: string[];
    correctOptionIds: number[];
  }> = [];

  private msgCounter = 1000;
  private pollCounter = 1;

  async sendPoll(
    _chatId: number | string,
    question: string,
    options: string[],
    other?: Record<string, any>
  ) {
    const messageId = this.msgCounter++;
    const pollId = `real_poll_${this.pollCounter++}`;
    this.polls.push({
      pollId,
      messageId,
      question,
      options,
      correctOptionIds: other?.correct_option_ids,
    });
    return {
      message_id: messageId,
      poll: { id: pollId },
    };
  }

  async stopPoll(_chatId: number | string, _messageId: number) {
    return { is_closed: true };
  }

  async sendMessage(_chatId: number | string, text: string) {
    this.messages.push(text);
    return { message_id: this.msgCounter++, text };
  }
}

async function runE2ESimulation() {
  console.log("🧪 2 ISHTIROKCHILI BOSHDAN-OXIRIGACHA QUIZ SINOVI BOSHLANDI...\n");

  const qm = new QuizManager();
  const api = new E2ETestApi();
  const testChatId = -100998877;

  // 1. Quizni boshlash
  console.log("1-qadam: Guruh admini tomonidan quiz boshlanishi...");
  const startResult = await qm.startQuiz(testChatId, sampleChemistryQuiz, api);
  assert.strictEqual(startResult.success, true);
  assert.ok(api.messages[0].includes("JDA Kimyo — namuna"));
  console.log("✅ Quiz e'loni guruhga yuborildi.\n");

  // 2. Savollarni ketma-ket o'tkazish va 2 ishtirokchi javob berishi
  const user1 = { id: 1001, first_name: "Ali <Kimyogar>", username: "ali_chem" };
  const user2 = { id: 1002, first_name: "Vali & Do'stlar" };

  for (let i = 0; i < sampleChemistryQuiz.questions.length; i++) {
    const q = sampleChemistryQuiz.questions[i];
    console.log(`2-qadam: ${i + 1}-savol («${q.question}») yuborilmoqda...`);

    await qm.sendNextQuestion(testChatId, api);
    const currentPoll = api.polls[api.polls.length - 1];
    assert.ok(currentPoll, "Poll yuborildi");
    assert.deepStrictEqual(currentPoll.correctOptionIds, [q.correctOptionId]);

    // Ishtirokchi 1 (Ali) to'g'ri javob beradi
    const a1 = qm.handlePollAnswer({
      pollId: currentPoll.pollId,
      user: user1,
      optionIds: [q.correctOptionId],
    });
    assert.strictEqual(a1, true, "Ali javobi qabul qilindi");

    // Takroriy javob elanishi tekshiriladi
    const a1Dup = qm.handlePollAnswer({
      pollId: currentPoll.pollId,
      user: user1,
      optionIds: [q.correctOptionId],
    });
    assert.strictEqual(a1Dup, false, "Ali'ning takroriy javobi rad etildi");

    // Ishtirokchi 2 (Vali): 4 ta to'g'ri, 1 ta noto'g'ri beradi
    const isValiCorrect = i !== 2; // 3-savolda Vali adashadi
    const valiOption = isValiCorrect ? q.correctOptionId : (q.correctOptionId + 1) % q.options.length;

    const a2 = qm.handlePollAnswer({
      pollId: currentPoll.pollId,
      user: user2,
      optionIds: [valiOption],
    });
    assert.strictEqual(a2, true, "Vali javobi qabul qilindi");

    console.log(`✅ ${i + 1}-savolga 2 ishtirokchi javob berdi.\n`);
  }

  // 3. Savollar tugashi va yakuniy reyting
  console.log("3-qadam: Quiz yakunlanishi va reyting...");
  await qm.sendNextQuestion(testChatId, api); // Savollar tugaganini anglatuvchi chaqiruv

  assert.strictEqual(qm.isQuizRunning(testChatId), false, "Quiz yakunlandi");

  const finalMessage = api.messages[api.messages.length - 1];
  console.log("Yakuniy guruh xabari:\n------------------------------------");
  console.log(finalMessage);
  console.log("------------------------------------\n");

  // Reytingni tekshirish
  assert.ok(finalMessage.includes("«JDA Kimyo — namuna» yakunlandi!"));
  assert.ok(finalMessage.includes("🥇 <b>@ali_chem</b>: 5/5 ball"));
  assert.ok(
    finalMessage.includes("🥈 <b>Vali &amp; Do&#039;stlar</b>: 4/5 ball"),
    "HTML xavfsiz escape qilingan bo'lishi kerak"
  );
  assert.ok(finalMessage.includes("jami javob vaqti:"));
  assert.ok(!finalMessage.includes("<Kimyogar>"), "Xom HTML teglari xabarga kirmagan bo'lishi kerak");

  console.log("🎉 2 ISHTIROKCHILI BOSHDAN-OXIRIGACHA SINOV 100% MUVAFFAQIYATLI O'TDI!");
}

runE2ESimulation().catch((err) => {
  console.error("❌ E2E testda xatolik:", err);
  process.exit(1);
});
