import { Quiz, QuizQuestion } from "./types.js";

/**
 * Dinshunoslik fanidan 80 ta savol — 20 tadan 4 ta qismga bo'lingan (DH1–DH4).
 * Manba: «Dinshunoslik fanidan testlar» to'plamining boshidan 80 ta savoli (#1–#80).
 * Test tuzuvchisi: Diyorbek Hasanov (@Dr_xasanov07)
 * Har bir savolga 20 soniya beriladi. Faqat guruhlarda o'tkaziladi.
 */

const DH_AUTHOR = "Diyorbek Hasanov (@Dr_xasanov07)";

function makeDhQuiz(
  id: string,
  title: string,
  description: string,
  questions: QuizQuestion[]
): Quiz {
  return {
    id,
    title,
    description,
    groupOnly: true,
    shuffle: true,
    bolim: "dinshunoslik",
    source: "",
    author: DH_AUTHOR,
    questions,
  };
}

export const dh1Questions: QuizQuestion[] = [
  {
    id: "dh1_1",
    question: "Muhammad s.a.v. qachon o‘zini Allohning rasuli (elchisi) deb e’lon qildi?",
    options: ["610 y", "622 y", "570 y", "632 y"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_2",
    question: "Ja’fariya qaysi yo‘nalishga mansub?",
    options: ["Shia", "Sunniylik", "Xavorijlar", "Mutaziliya"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_3",
    question: "Buddizm dini qachon paydo bo‘ldi?",
    options: [
      "Milodimizdan avv. V asrda",
      "Milodimizdan avv. VI–V asrda",
      "Milodimizning I asrida",
      "Milodimizgacha XIII asrda",
    ],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_4",
    question: "Islom dinida Xulofoi Roshidinlar ko‘rsatilgan javobni toping?",
    options: [
      "Abu Bakr, Umar, Usmon, Ali",
      "Muhammad, Ali, Xasan, Xusan",
      "Abu Xurayro, Ibn Hanbal, Ibn Xoshim",
      "Ibrohim, Muso, Iso, Dovud",
    ],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_5",
    question: "Vatikan davlati nasroniylikdagi qaysi oqimning markazi hisoblanadi?",
    options: [
      "Katolikning",
      "Pravoslavlikning",
      "Protestantlikning",
      "Baptistlikning",
    ],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_6",
    question: "Qur’onda nechta sura bor?",
    options: ["114", "110", "115", "286"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_7",
    question: "Buddizmda ishongan kishining asosiy maqsadi nima?",
    options: [
      "«Muqaddas qadamjo»larga sig‘inish",
      "Rohiblikni qabul qilish",
      "Qayta tug‘ilish zanjiridan o‘tish",
      "Ilohlarga sig‘inish",
    ],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_8",
    question: "Buddaviylik dinining asoschisi Siddxarta Gautama kim bo‘lgan?",
    options: ["Dehqon", "Cho‘pon", "Savdogar", "Shahzoda"],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_9",
    question: "Quyidagilardan qaysi biri dinning jamiyatda bajaradigan vazifalaridan emas?",
    options: [
      "Tasalli berish, to‘ldirish",
      "Qonuniylashtirish",
      "Boshqarish",
      "Qiynash",
    ],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_10",
    question: "Xristianlikning muqaddas manbasi?",
    options: ["Injil", "Qadimgi ahd", "Talmud", "Zabur"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_11",
    question: "Islom dini qachon paydo bo‘ldi?",
    options: [
      "Milodgacha V asrda",
      "Milodning I asrida",
      "Milodning VII asrida",
      "Milodning VI asrda",
    ],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_12",
    question: "O‘zining kelib chiqishini o‘simliklar yoki hayvonlarning ma’lum bir turlaridan kelib chiqqan deb hisoblovchi eng qadimgi diniy ta’limot qanday nomlanadi?",
    options: ["Totemizm", "Fetishizm", "Animizm", "Magiya"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_13",
    question: "O‘zbekistonda qancha konfessiya mavjud?",
    options: ["16 ta", "18 ta", "20 ta", "15 ta"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_14",
    question: "Islom dinining asosiy bayramlari qaysilar?",
    options: [
      "Pasxa, Rojdestvo",
      "Xatna, nikoh",
      "Navro‘z, Mavlud",
      "Ramazon hayiti, Qurbon hayiti",
    ],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_15",
    question: "S. Gautama necha yoshida saroyni tark qiladi?",
    options: ["30 yosh", "33 yosh", "40 yosh", "20 yosh"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_16",
    question: "Bibliyaning xristianlikka oid qismi qanday nomlanadi?",
    options: ["Yangi ahd", "Eski ahd", "Injil", "Tavrot"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_17",
    question: "Ilk ibtidoiy diniy tasavvurlarda sehrgarlik qanday nomlangan?",
    options: ["Totemizm", "Fetishizm", "Animizm", "Magiya"],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_18",
    question: "Muhammad s.a.v. payg‘ambar tug‘ilgan kuniga bag‘ishlangan bayramning nomi qanday ataladi?",
    options: ["Xatna", "Qurbon hayit", "Ramazon hayit", "Mavlud"],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_19",
    question: "«Xushxabar» deb tarjima qilingan nasroniylikning muqaddas kitoblaridan biri...?",
    options: ["Injil", "Muqaddas yozuvlar", "Apokalipsis", "Tavrot"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh1_20",
    question: "Din so‘zining ma’nosi qanday?",
    options: ["Quvonch", "Ishonch", "Ezgulik", "Mukofot"],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
];

export const dh2Questions: QuizQuestion[] = [
  {
    id: "dh2_1",
    question: "S. Gautama haqiqatni anglashda necha kun daraxt tagida o‘tirdi?",
    options: ["44 kun", "49 kun", "55 kun", "30 kun"],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_2",
    question: "Islom dinining Muqaddas kitobi nima deb ataladi?",
    options: ["Avesto", "Qur’on", "Tripitaka", "Tavrot"],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_3",
    question: "Islomda ro‘za necha kun tutiladi?",
    options: ["70 kun", "33 kun", "30 kun", "40 kun"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_4",
    question: "Buddaviylik dinida inson erishishi mumkin bo‘lgan oliy daraja qanday nomlanadi?",
    options: ["Rohib", "Ruhoniy", "Ravvin", "Nirvana"],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_5",
    question: "Odamlar guruhi (urug‘i, qabilasi) bilan hayvon va o‘simliklarning muayyan turi o‘rtasida g‘ayritabiiy aloqadorlik, qon-qarindoshlik borligi to‘g‘risidagi ishonch (e’tiqod) qaysi dinning xususiyati?",
    options: ["Fetishizm", "Totemizm", "Animizm", "Magiya"],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_6",
    question: "Qaysi din ta’limotida inson vafotidan keyin boshqa narsa ko‘rinishida qayta tug‘iladi?",
    options: ["Buddaviylik", "Zardushtiylik", "Yahudiylik", "Xristianlik"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_7",
    question: "E’tiqod qiluvchilarning soniga ko‘ra eng katta jahon dini qaysi?",
    options: ["Xristianlik", "Buddizm", "Islom", "Hinduiylik"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_8",
    question: "Islom dinida qanday yo‘nalishlari bor?",
    options: [
      "Modernizm va fundamentalizm",
      "Ismoiliylik va vahobiylik",
      "Sunniylik va shialik",
      "Bahoiylik va bobiylik",
    ],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_9",
    question: "Buddaviylikda Budda o‘tirgan daraxt qanday nomlandi?",
    options: ["Trishna", "Mayya", "Botxa", "Gautama"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_10",
    question: "Xristianlikning qaysi oqimi G‘arbiy Yevropa va Lotin Amerikasida eng ko‘p tarqalgan?",
    options: ["Katolitsizm", "Pravoslavie", "Baptizm", "Protestantsizm"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_11",
    question: "Dinning ibtidoiy shakllari qaysilar?",
    options: [
      "Magiya, iudaizm, jaynizm, zorastrizm",
      "Fetishizm, totemizm, magiya, animizm",
      "Fetishizm, buddizm, qabila boshliqlarining shaxsiga sig‘inish",
      "Xristianlik, totemizm, sintoizm, tabiatni ilohiylashtirish",
    ],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_12",
    question: "Buddaga dastlab necha kishi hamroh bo‘ladi?",
    options: ["5 kishi", "6 kishi", "7 kishi", "8 kishi"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_13",
    question: "Xristianlik dinida protestantizm oqimi qachon ajralib chiqqan?",
    options: ["1517 yilda", "1054 yilda", "1534 yilda", "1532 yilda"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_14",
    question: "Odamlarga, narsalarga va atrof olamdagi hodisalarga g‘ayritabiiy yo‘l bilan ta’sir qilish mumkinligiga bo‘lgan ishonch asosidagi e’tiqodlar va marosimlar qaysi dinning xususiyati?",
    options: ["Totemizm", "Fetishizm", "Magiya", "Animizm"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_15",
    question: "Buddaviylik dinida azoblardan qutulish uchun inson qanday holatga erishishi kerak?",
    options: ["Meditatsiya", "Donolik", "Trishna", "Nirvana"],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_16",
    question: "«Yetti sirli marosim» qaysi dinga tegishli?",
    options: ["Xristianlik", "Hinduiylik", "Buddizm", "Sintoiylik"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_17",
    question: "Dinning kelib chiqishi haqidagi asosiy qarashlar quyidagilardan qaysi biri?",
    options: [
      "Diniy va ilmiy",
      "Idealistik va materialistik",
      "Nasroniylarcha va musulmonlarcha",
      "Metafizik va dialektik",
    ],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_18",
    question: "Vijdon erkinligi va diniy tashkilotlar to‘g‘risidagi qonun qachon qabul qilingan?",
    options: [
      "2020-yil 1-avgust",
      "2019-yil 1-sentabr",
      "2022-yil 14-iyun",
      "2021-yil 4-may",
    ],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_19",
    question: "Pravoslav cherkovi qachon mustaqil bo‘lgan?",
    options: ["1054-yilda", "395-yilda", "1448-yilda", "988-yilda"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh2_20",
    question: "Xristianlik dinida eng oxirida vujudga kelgan yo‘nalish qaysi?",
    options: ["Protestantlik", "Katolik", "Pravoslav", "Baptizm"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
];

export const dh3Questions: QuizQuestion[] = [
  {
    id: "dh3_1",
    question: "Har xil buyumlar yoki tumorlarni balo-qazolardan asrovchi yoki baxt-saodatga erishtiruvchi eng qadimgi diniy ta’limot qanday nomlanadi?",
    options: ["Totemizm", "Fetishizm", "Animizm", "Magiya"],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_2",
    question: "Sintoiylik dini qaysi davlatda vujudga kelgan?",
    options: ["Yaponiya", "Xitoy", "Hindiston", "Tibet"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_3",
    question: "Yahudiylikda ibodatxona qanday nomlanadi?",
    options: ["Masjid", "Cherkov", "Sinagoga", "Iparxiya"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_4",
    question: "Jahonda e’tiqod qiluvchilari soni jihatidan eng katta milliy din qaysi?",
    options: ["Hinduizm", "Iudaizm", "Sintoizm", "Daosizm"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_5",
    question: "Konfutsiy ta’limotida qaysi muammolar asosiy o‘rin tutadi?",
    options: ["Ijtimoiy-axloqiy", "Falsafiy", "Estetik", "Siyosiy"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_6",
    question: "Daosizm qayerda paydo bo‘lgan?",
    options: ["Yaponiya", "Xitoy", "Hindiston", "Tibet"],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_7",
    question: "Konfutsiychilikning asoschisi kim?",
    options: ["Pan Gu", "Lao Szi", "Kun Szi", "Shan Di"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_8",
    question: "Sintoizmning bosh xudosi kim?",
    options: [
      "Quyosh ma’budasi Amaterasu",
      "Oxirgi payg‘ambar Jina",
      "Saqlovchi xudo Vishnu",
      "Yaratuvchi xudo Braxma",
    ],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_9",
    question: "Jaynizm qaysi davlatning milliy dinidir?",
    options: ["Yaponiyaning", "Xitoyning", "Hindistonning", "Mongoliyaning"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_10",
    question: "Yahudiylik ta’limotida ular bilishi kerak bo‘lgan ko‘rsatmalar qanchani tashkil etadi?",
    options: ["613 ta", "546 ta", "248", "365"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_11",
    question: "Yahudiylik ta’limotida ular bilishi kerak bo‘lgan taqiqlar qanchani tashkil etadi?",
    options: ["613 ta", "546 ta", "248", "365"],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_12",
    question: "Inson o‘zini o‘rab turgan muhitda ruhlarning mavjudligiga ishonuvchi eng qadimgi diniy ta’limot qanday nomlanadi?",
    options: ["Totemizm", "Fetishizm", "Animizm", "Magiya"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_13",
    question: "Hinduizm dinidagi oliy xudoni toping?",
    options: ["Shiva", "Braxma", "Vishnu", "Sinto"],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_14",
    question: "Konfutsiyning shogirdlari qancha bo‘lgan?",
    options: ["3 ming", "72 ta", "2,5 ming", "Shogirdlari bo‘lmagan"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_15",
    question: "Quyidagi milliy dinlarning qaysi samoviy dinlardan hisoblanadi?",
    options: ["Hinduizm", "Sintoizm", "Konfutsiylik", "Yahudiylik"],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_16",
    question: "Avesto qaysi dinning muqaddas kitobi hisoblanadi?",
    options: ["Islom", "Xristianlik", "Yahudiylik", "Zardushtiylik"],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_17",
    question: "Sinagoga so‘zining lug‘aviy ma’nosi nima?",
    options: [
      "Yig‘ilish",
      "Ibodatxona",
      "Alohida ajratilgan joy",
      "Marosim",
    ],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_18",
    question: "G‘arb nazariyasiga ko‘ra zardushtiylik dini qayerda vujudga kelgan?",
    options: ["Eronda", "Xorazmda", "Arabistonda", "Pokistonda"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_19",
    question: "Sharq nazariyasiga ko‘ra zardushtiylik dini qayerda vujudga kelgan?",
    options: ["Eronda", "Xorazmda", "Arabistonda", "Pokistonda"],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
  {
    id: "dh3_20",
    question: "Zardushtiylikning asosiy ta’limotiga aloqador bo‘lmagan javobni toping?",
    options: ["Ezgu fikr", "Ezgu so‘z", "Ezgu amal", "Ezgu niyat"],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
];

export const dh4Questions: QuizQuestion[] = [
  {
    id: "dh4_1",
    question: "Quyidagilarning qaysi biri zardushtiylikdagi muqaddas 4 unsurga kirmaydi?",
    options: ["Suv", "Olov", "Bulut", "Havo"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_2",
    question: "Xizbut-taxrir oqimiga qachon asos solingan?",
    options: ["1951-yil", "1952-yil", "1953-yil", "1954-yil"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_3",
    question: "12 ming qoramol terisiga yozilgan muqaddas kitob?",
    options: ["Avesto", "Injil", "Tavrot", "Qur’on"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_4",
    question: "Movarounnahrlik allomalarning qaysi biri Avestoning «30 nask»ligi to‘g‘risidagi ma’lumotlarni keltirib o‘tgan?",
    options: ["Ibn Sino", "Xorazmiy", "Beruniy", "Farg‘oniy"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_5",
    question: "Zardushtiylikdagi kunlik ibodatlar soni qancha?",
    options: ["3 ta", "4 ta", "5 ta", "6 ta"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_6",
    question: "Zardushtiylar orasida 3 yil yashab, ularning tarixini o‘rgangan olim kim?",
    options: ["Zamaxshariy", "Volter", "Dyuperron", "B. Axmedov"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_7",
    question: "Dinning jamiyatdagi vazifalari mazmunini qaysi qatorda noto‘g‘ri ko‘rsatilgan?",
    options: [
      "kompensator — tasalli beruvchilik",
      "integrator — birlashtiruvchilik",
      "legitimizatsiya — nazorat qiluvchilik",
      "kommunikativ — bog‘lashtiruvchi",
    ],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_8",
    question: "Qaysi dinda vafot etganlarning suyaklari maxsus idishda saqlanadi?",
    options: ["Zardushtiylik", "Xristianlik", "Hinduizm", "Yahudiylik"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_9",
    question: "«Hamma uchun vijdon erkinligi kafolatlanadi. Har bir inson xohlagan dinga e’tiqod qilish yoki hech qaysi dinga e’tiqod qilmaslik huquqiga ega. Diniy qarashlarni majburan singdirishga yo‘l qo‘yilmaydi». Bu qonun Konstitutsiyamizning qaysi moddada keltirilgan?",
    options: ["35-modda", "57-modda", "61-modda", "18-modda"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_10",
    question: "«Ettinchi kun adventistlari» oqimi nechanchi yil tuzilgan?",
    options: ["1844", "1860", "1863", "1850"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_11",
    question: "Quyidagi harakatlardan qaysi biri Eronda vujudga kelgan?",
    options: ["Marifatchilar", "Baxshillochilar", "Shohidiylar", "Bahoiylar"],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_12",
    question: "ISESCO tomonidan Toshkent shahriga «Islom madaniyatining poytaxti» maqomi berildi?",
    options: ["2007", "2008", "2009", "2010"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_13",
    question: "Quyidagilardan qaysi biri Hinduizmdagi ilohlardan emas?",
    options: ["Shiva", "Vishnu", "Braxma", "Sinto"],
    correctOptionId: 3,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_14",
    question: "Qaysi ta’limot 24 ta Payg‘ambar yoki avliyo tomonidan asos solingan?",
    options: ["Sikhiylik", "Veda", "Jaynizim", "Daosizm"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_15",
    question: "Sintoizm dini qayerda vujudga kelgan?",
    options: ["Korea", "Xitoy", "Yaponiya", "Eron"],
    correctOptionId: 2,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_16",
    question: "Konfutsiylikka kim asos solgan?",
    options: ["Kun szi", "Min", "Kim in", "Lao Szi"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_17",
    question: "O‘zbekistonda diniy tashkilotlar, muassasalar qaysi organ tomonidan ro‘yxatga olinadi?",
    options: [
      "Adliya vazirligi",
      "Mudofaa vazirligi",
      "Ichki ishlar vazirligi",
      "Tashqi ishlar vazirligi",
    ],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_18",
    question: "O‘zbekiston Respublikasi Vazirlar Mahkamasi huzuridagi O‘zbekiston Islom sivilizatsiyasi markazi qachon tashkil etildi?",
    options: ["2018", "2017", "2016", "2015"],
    correctOptionId: 1,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_19",
    question: "Hozir BMTning terrorizmga qarshi turishga qaratilgan nechta hujjat bor?",
    options: ["13 ta", "14 ta", "15 ta", "16 ta"],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
  {
    id: "dh4_20",
    question: "Nabiy bilan rasulni orasidagi farqni toping?",
    options: [
      "Nabiy avvalgi shariatni davom ettiradi, rasulga yangi shariat tushadi.",
      "Nabiy yangi shariat tushadi. Rasulga avvalgi shariatni davom etadi",
      "Nabiyga rasulga ham yangi shariat tushadi",
      "Nabiy ham rasul ham avvalgi shariatni davom etadi",
    ],
    correctOptionId: 0,
    timeLimitSeconds: 20,
  },
];

export const dh1Quiz = makeDhQuiz(
  "DH1",
  "Dinshunoslik — 1-qism (DH1)",
  "1–20-savollar: Dinshunoslik asoslari, ibtidoiy dinlar, buddizm, xristianlik va islom asoslari (20s/savol)",
  dh1Questions
);

export const dh2Quiz = makeDhQuiz(
  "DH2",
  "Dinshunoslik — 2-qism (DH2)",
  "21–40-savollar: Jahon dinlari, ibtidoiy shakllar va vijdon erkinligi qonunchiligi (20s/savol)",
  dh2Questions
);

export const dh3Quiz = makeDhQuiz(
  "DH3",
  "Dinshunoslik — 3-qism (DH3)",
  "41–60-savollar: Milliy dinlar va zardushtiylik asoslari (20s/savol)",
  dh3Questions
);

export const dh4Quiz = makeDhQuiz(
  "DH4",
  "Dinshunoslik — 4-qism (DH4)",
  "61–80-savollar: Zardushtiylik, diniy oqimlar va O‘zbekiston qonunchiligi (20s/savol)",
  dh4Questions
);

export const allDhQuizzes: Quiz[] = [dh1Quiz, dh2Quiz, dh3Quiz, dh4Quiz];
