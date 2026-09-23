import { Quiz } from "./types.js";

export const sampleChemistryQuiz: Quiz = {
  id: "jda-chem-sample-1",
  title: "JDA Kimyo — namuna",
  description: "Kimyo fanidan boshlang'ich bilimlar bo'yicha 5 savolli sinov quizi",
  questions: [
    {
      id: "q1",
      question: "1. Suvning (H₂O) molar massasi qancha?",
      options: ["16 g/mol", "18 g/mol", "20 g/mol", "22 g/mol"],
      correctOptionId: 1, // "18 g/mol"
      explanation: "Vodorod (H) = 1 g/mol, Kislorod (O) = 16 g/mol. H₂O = 1×2 + 16 = 18 g/mol.",
      timeLimitSeconds: 15,
    },
    {
      id: "q2",
      question: "2. Davriy jadvalda tartib raqami 6 bo'lgan kimyoviy element qaysi?",
      options: ["Azot (N)", "Kislorod (O)", "Uglerod (C)", "Bor (B)"],
      correctOptionId: 2, // "Uglerod (C)"
      explanation: "Uglerodning atom raqami 6 bo'lib, davriy jadvalning 2-davr, IV guruhida joylashgan.",
      timeLimitSeconds: 15,
    },
    {
      id: "q3",
      question: "3. Osh tuzining kimyoviy formulasi qaysi?",
      options: ["NaCl", "KCl", "NaOH", "CaCO₃"],
      correctOptionId: 0, // "NaCl"
      explanation: "Osh tuzi — natriy xlorid (NaCl) ning maishiy nomidir.",
      timeLimitSeconds: 15,
    },
    {
      id: "q4",
      question: "4. Yer atmosferasi havosining taxminan 78% qismini qaysi gaz tashkil qiladi?",
      options: ["Kislorod (O₂)", "Azot (N₂)", "Karbonat angidrid (CO₂)", "Argon (Ar)"],
      correctOptionId: 1, // "Azot (N₂)"
      explanation: "Havo tarkibining taxminan 78% qismini azot (N₂), 21% qismini kislorod (O₂) tashkil qiladi.",
      timeLimitSeconds: 15,
    },
    {
      id: "q5",
      question: "5. Kislotali muhitda lakmus indikatori qanday rangga kiradi?",
      options: ["Ko'k", "Yashil", "Qizil", "Binafsha"],
      correctOptionId: 2, // "Qizil"
      explanation: "Lakmus kislotali muhitda qizil rangga, ishqoriy muhitda esa ko'k rangga o'zgaradi.",
      timeLimitSeconds: 15,
    },
  ],
};
