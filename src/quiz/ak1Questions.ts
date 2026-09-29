import path from "path";
import { Quiz } from "./types.js";

const ASSETS_DIR = path.resolve(process.cwd(), "assets", "amino_acids");

/**
 * 329–330-betlardagi 17-jadval asosida 21 ta aminokislotaning
 * kimyoviy formulalari bo'yicha interaktiv rasm-quiz (AK1).
 *
 * Savollar va variantlar har sessiyada aralashtiriladi.
 * Har bir savolga 30 soniya beriladi.
 * Test yaratuvchisi: @diyorbek_jabborov
 * Manba: 329–330-betlardagi 17-jadval
 */
export const ak1Quiz: Quiz = {
  id: "AK1",
  title: "Aminokislotalar strukturasi (AK1)",
  description: "329–330-betlardagi 17-jadval asosida 21 ta aminokislotaning kimyoviy formulalari bo'yicha interaktiv rasm-quiz",
  groupOnly: true,
  shuffle: true,
  source: "329–330-betlardagi 17-jadval",
  questions: [
    {
      id: "ak1_1",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_1.png"),
      options: ["Glitsin", "Alanin", "Valin", "Serin"],
      correctOptionId: 0, // Glitsin
      explanation: "Glitsin (Gli.) — eng sodda aminokislota, formulasi: NH2—CH2—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_2",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_2.png"),
      options: ["Glitsin", "Alanin", "Valin", "Leysin"],
      correctOptionId: 1, // Alanin
      explanation: "Alanin (Ala.) — α-aminopropion kislota, formulasi: CH3—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_3",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_3.png"),
      options: ["Valin", "Alanin", "Leysin", "Izoleysin"],
      correctOptionId: 0, // Valin
      explanation: "Valin (Val.) — α-aminoisovalerian kislota, izopropil radikaliga ega: CH3—CH(CH3)—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_4",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_4.png"),
      options: ["Izoleysin", "Valin", "Leysin", "Lizin"],
      correctOptionId: 2, // Leysin
      explanation: "Leysin (Ley.) — α-aminoisokapron kislota, 4-uglerodida metil guruhi tarmoqlangan: CH3—CH(CH3)—CH2—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_5",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_5.png"),
      options: ["Leysin", "Izoleysin", "Valin", "Treonin"],
      correctOptionId: 1, // Izoleysin
      explanation: "Izoleysin (Iley.) — α-amino-β-metilvalerian kislota, 3-uglerodida metil guruhi joylashgan: CH3—CH2—CH(CH3)—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_6",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_6.png"),
      options: ["Asparagin kislota", "Glutamin kislota", "Alanin", "Serin"],
      correctOptionId: 0, // Asparagin kislota
      explanation: "Asparagin kislota (Asp.) — dikarboksilli 4 uglerodli aminokislota (bitta —CH2— guruhi mavjud): HOOC—CH2—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_7",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_7.png"),
      options: ["Asparagin kislota", "Glutamin kislota", "Ornitin", "Valin"],
      correctOptionId: 1, // Glutamin kislota
      explanation: "Glutamin kislota (Glu.) — dikarboksilli 5 uglerodli aminokislota (ikkita —CH2— guruhi mavjud): HOOC—CH2—CH2—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_8",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_8.png"),
      options: ["Lizin", "Ornitin", "Arginin", "Gistidin"],
      correctOptionId: 1, // Ornitin
      explanation: "Ornitin (Ori.) — α,δ-diaminovalerian kislota (5 ta uglerod, ikkita amino guruh): CH2(NH2)—(CH2)2—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_9",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_9.png"),
      options: ["Ornitin", "Lizin", "Arginin", "Leysin"],
      correctOptionId: 1, // Lizin
      explanation: "Lizin (Liz.) — α,ε-diaminokapron kislota (6 ta uglerod, to'rtta —CH2— zanjiriga ega): NH2—(CH2)4—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_10",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_10.png"),
      options: ["Serin", "Treonin", "Sistein", "Alanin"],
      correctOptionId: 0, // Serin
      explanation: "Serin (Ser.) — α-amino-β-gidroksipropion kislota, birlamchi spirt guruhi —CH2OH ga ega: HOCH2—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_11",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_11.png"),
      options: ["Serin", "Treonin", "Valin", "Izoleysin"],
      correctOptionId: 1, // Treonin
      explanation: "Treonin (Tre.) — α-amino-β-gidroksimoy kislota, ikkilamchi spirt guruhi >CH—OH ga ega: CH3—CH(OH)—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_12",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_12.png"),
      options: ["Sistein", "Sistin", "Metionin", "Serin"],
      correctOptionId: 0, // Sistein
      explanation: "Sistein (Sis.-n) — α-amino-β-tiopropion kislota, tiol —SH guruhiga ega monomer: HS—CH2—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_13",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_13.png"),
      options: ["Sistein", "Sistin", "Metionin", "Lizin"],
      correctOptionId: 1, // Sistin
      explanation: "Sistin (Sis.) — ikki molekula sisteinning disulfid —S—S— ko'prigi orqali bog'lanishidan hosil bo'lgan dimer: [S—CH2—CH(NH2)COOH]2.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_14",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_14.png"),
      options: ["Metionin", "Sistein", "Sistin", "Glutamin kislota"],
      correctOptionId: 0, // Metionin
      explanation: "Metionin (Met.) — tarkibida tioefir —S—CH3 guruhi tutgan muhim aminokislota: CH3—S—CH2—CH2—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_15",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_15.png"),
      options: ["Fenilalanin", "Tirozin", "Triptofan", "Gistidin"],
      correctOptionId: 0, // Fenilalanin
      explanation: "Fenilalanin (Fen.) — α-amino-β-fenilpropion kislota, oddiy fenil halqasiga ega: C6H5—CH2—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_16",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_16.png"),
      options: ["Fenilalanin", "Tirozin", "Triptofan", "Treonin"],
      correctOptionId: 1, // Tirozin
      explanation: "Tirozin (Tir.) — α-amino-β-(para-gidroksifenil)propion kislota, fenol —OH guruhiga ega: HO—C6H4—CH2—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_17",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_17.png"),
      options: ["Triptofan", "Gistidin", "Prolin", "Tirozin"],
      correctOptionId: 0, // Triptofan
      explanation: "Triptofan (Tri.) — indol geterohalqasiga (benzol + pirrol) ega aromatik aminokislota: Indol—CH2—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_18",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_18.png"),
      options: ["Prolin", "Oksiprolin", "Gistidin", "Triptofan"],
      correctOptionId: 0, // Prolin
      explanation: "Prolin (Pro.) — pirrolidin halqasiga ega geterosiklik ikkilamchi aminokislota (iminokislota): Pirrolidin-2-karbon kislota.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_19",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_19.png"),
      options: ["Prolin", "Oksiprolin", "Gistidin", "Tirozin"],
      correctOptionId: 1, // Oksiprolin
      explanation: "Oksiprolin (Pro-OH) — pirrolidin halqasining 4-holatida gidroksil —OH guruhi tutgan hosila: 4-gidroksipirrolidin-2-karbon kislota.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_20",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_20.png"),
      options: ["Gistidin", "Arginin", "Prolin", "Triptofan"],
      correctOptionId: 0, // Gistidin
      explanation: "Gistidin (Gis.) — imidazol geterohalqasiga ega asosli aminokislota: Imidazol—CH2—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
    {
      id: "ak1_21",
      question: "Rasmdagi aminokislota qaysi?",
      imagePath: path.join(ASSETS_DIR, "ak_21.png"),
      options: ["Lizin", "Arginin", "Ornitin", "Gistidin"],
      correctOptionId: 1, // Arginin
      explanation: "Arginin (Arg.) — kuchli asosli guanidin guruhiga ega aminokislota: NH2—C(=NH)—NH—(CH2)3—CH(NH2)—COOH.",
      timeLimitSeconds: 30,
    },
  ],
};
