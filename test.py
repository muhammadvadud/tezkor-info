from django.db import transaction
# !!! Model joylashgan joyni o'zgartiring !!!
from core.apps.main.models import CategoryModel

# =============================================================================
# OKED KATEGORIYALARI RO'YXATI (TO'LIQ PDF asosida)
# Format: (code, uz_name, ru_name, en_name)
# =============================================================================
OKED_TRIPLE_CATEGORIES = [
    # SECTOR 1
    ("SECTOR_1", "Qishloq xo'jaligi, o'rmonchilik va baliqchilik", "СЕЛЬСКОЕ ХОЗЯЙСТВО, ЛЕСОВОДСТВО И РЫБОЛОВСТВО",
     "Agriculture, Forestry and Fishing"),
    ("01", "Ekinchilik va chorvachilik, ovchilik va ushbu sohalarda xizmat ko'rsatish",
     "Растениеводство и Животноводство, Охота и предоставление услуг в этих областях",
     "Crop and animal production, hunting and related service activities"),
    ("01.1", "Mavsumiy ekinlarni yetishtirish", "Выращивание сезонных культур", "Growing of non-perennial crops"),
    ("01.11", "Donda ekinlarni (guruchdan tashqari), dukkakli ekinlar va moyli urug'larni yetishtirish",
     "Выращивание зерновых культур (за исключением риса), бобовых культур и масличных семян",
     "Growing of cereals (except rice), leguminous crops and oil seeds"),
    ("01.11.1", "Donda ekinlarni yetishtirish (guruchdan tashqari)", "Выращивание зерновых культур (кроме риса)",
     "Growing of cereals (except rice)"),
    ("01.11.2", "Dukkakli ekinlarni yetishtirish", "Выращивание бобовых культур", "Growing of leguminous crops"),
    ("01.11.3", "Moyli ekinlarni va ularning urug'larini yetishtirish",
     "Выращивание масличных культур va ularning urug'larini", "Growing of oil seeds and their seeds"),
    ("01.12", "Guruch yetishtirish", "Выращивание риса", "Growing of rice"),
    ("01.12.0", "Guruch yetishtirish", "Выращивание риса", "Growing of rice"),
    # Ikkilanishni tekshirish uchun qoldiramiz
    ("01.13", "Sabzavot va poliz ekinlarini, ildizmevalilarni va tugunakmevalilarni yetishtirish",
     "Выращивание овощей и бахчевых, корнеплодов и клубнеплодов",
     "Growing of vegetables, melons and gourds, root and tuber crops"),
    ("01.13.1", "Sabzavotlarni yetishtirish", "Выращивание овощей", "Growing of vegetables"),
    ("01.13.2", "Poliz ekinlarini yetishtirish", "Выращивание бахчевых культур", "Growing of melons and gourds"),
    ("01.13.3", "Kraxmalli va inulinli ildizmevalilarni, tugunakmevalilarni va ularning urug'larini yetishtirish",
     "Выращивание корнеплодов va tugunakmevalilarni kraxmal va inulin miqdori yuqori bo'lgan urug'lar",
     "Growing of root and tuber crops with high starch and inulin content and their seeds"),
    ("01.13.9",
     "Boshqa ildizmevalilarni, tugunakmevalilarni va ularning urug'larini, qo'ziqorin va trufellarni yetishtirish",
     "Выращивание прочих корне- и клубнеплодных культур и их семян, грибов и трюфелей",
     "Growing of other root and tuber crops and their seeds, fungi and truffles"),
    ("01.14", "Qand qamishi yetishtirish", "Выращивание сахарного тростника", "Growing of sugar cane"),
    ("01.14.0", "Qand qamishi yetishtirish", "Выращивание сахарного тростника", "Growing of sugar cane"),
    ("01.15", "Tamaki yetishtirish", "Выращивание табака", "Growing of tobacco"),
    ("01.15.0", "Tamaki yetishtirish", "Выращивание табака", "Growing of tobacco"),
    ("01.16", "Tolali ip yigirish ekinlarini yetishtirish", "Выращивание волокнистых прядильных культур",
     "Growing of fibrous spinning crops"),
    ("01.16.1", "Paxta yetishtirish", "Выращивание хлопчатника", "Growing of cotton"),
    ("01.16.2", "Zig'ir yetishtirish", "Выращивание льна", "Growing of flax"),
    ("01.16.9", "Boshqa tolali (lubyanoy) ekinlarni yetishtirish", "Выращивание прочих прядильных (лубяных) культур",
     "Growing of other fibrous (bast) crops"),
    ("01.19", "Boshqa mavsumiy ekinlarni yetishtirish", "Выращивание прочих сезонных культур",
     "Growing of other non-perennial crops"),
    ("01.19.1", "Ozuqa ekinlarini va ularning urug'larini yetishtirish", "Выращивание кормовых культур и их семян",
     "Growing of fodder crops and their seeds"),
    ("01.19.2", "Gullar va ularning urug'larini yetishtirish", "Выращивание цветов и ularning urug'larini",
     "Growing of flowers and their seeds"),
    ("01.19.9", "Boshqa toifaga kiritilmagan ko'p yillik bo'lmagan ekinlarni yetishtirish",
     "Выращивание прочих не многолетних культур, не включенных в другие категории",
     "Growing of other non-perennial crops not elsewhere classified"),

    ("01.2", "Ko'p yillik ekinlarni yetishtirish", "Выращивание многолетних культур", "Growing of perennial crops"),
    ("01.21", "Uzum yetishtirish", "Выращивание винограда", "Growing of grapes"),
    ("01.21.0", "Uzum yetishtirish", "Выращивание винограда", "Growing of grapes"),
    ("01.22", "Tropik va subtropik mevalarni yetishtirish", "Выращивание тропических va subtropik mevalar",
     "Growing of tropical and subtropical fruits"),
    ("01.22.0", "Tropik va subtropik mevalarni yetishtirish", "Выращивание тропических va subtropik mevalar",
     "Growing of tropical and subtropical fruits"),
    ("01.23", "Sitrussimon mevalarni yetishtirish", "Выращивание цитрусовых фруктов", "Growing of citrus fruits"),
    ("01.23.0", "Sitrussimon mevalarni yetishtirish", "Выращивание цитрусовых фруктов", "Growing of citrus fruits"),
    ("01.24", "Danakli va urug'li mevalarni yetishtirish", "Выращивание косточковых va urug'li mevalar",
     "Growing of pome and stone fruits"),
    ("01.24.0", "Danakli va urug'li mevalarni yetishtirish", "Выращивание косточковых va urug'li mevalar",
     "Growing of pome and stone fruits"),
    ("01.25", "Boshqa mevali daraxtlar, butalar va yong'oqlarni yetishtirish",
     "Выращивание прочих видов плодовых деревьев, кустарников и орехов",
     "Growing of other fruit trees, bushes and nuts"),
    ("01.25.0", "Boshqa mevali daraxtlar, butalar va yong'oqlarni yetishtirish",
     "Выращивание прочих видов плодовых деревьев, кустарников и орехов",
     "Growing of other fruit trees, bushes and nuts"),
    ("01.26", "Moyli mevalarni yetishtirish", "Выращивание масленичных фруктов", "Growing of oil seeds"),
    ("01.26.0", "Moyli mevalarni yetishtirish", "Выращивание масленичных фруктов", "Growing of oil seeds"),
    ("01.27", "Ichimliklar ishlab chiqarish uchun ekinlarni yetishtirish",
     "Выращивание культур для производства напитков", "Growing of beverage crops"),
    ("01.27.0", "Ichimliklar ishlab chiqarish uchun ekinlarni yetishtirish",
     "Выращивание культур для производства напитков", "Growing of beverage crops"),
    ("01.28", "Ziravorlar, xushbo'y, kuchli ta'sir qiluvchi narkotik va farmatsevtik ekinlarni yetishtirish",
     "Выращивание специй, ароматических, сильнодействующих narkotik va farmatsevtik ekinlar",
     "Growing of spices, aromatic, strongly narcotic and pharmaceutical crops"),
    ("01.28.0", "Ziravorlar, xushbo'y, kuchli ta'sir qiluvchi narkotik va farmatsevtik ekinlarni yetishtirish",
     "Выращивание специй, ароматических, сильнодействующих narkotik va farmatsevtik ekinlar",
     "Growing of spices, aromatic, strongly narcotic and pharmaceutical crops"),
    ("01.29", "Boshqa ko'p yillik ekinlarni yetishtirish", "Выращивание прочих многолетних культур",
     "Growing of other perennial crops"),
    ("01.29.0", "Boshqa ko'p yillik ekinlarni yetishtirish", "Выращивание прочих многолетних культур",
     "Growing of other perennial crops"),

    ("01.3", "Fermer xo'jaliklari mahsulotlarini ishlab chiqarish", "Производство продукции питомников",
     "Plant propagation"),
    ("01.30", "Fermer xo'jaliklari mahsulotlarini ishlab chiqarish", "Производство продукции питомников",
     "Plant propagation"),
    ("01.30.0", "Fermer xo'jaliklari mahsulotlarini ishlab chiqarish", "Производство продукции питомников",
     "Plant propagation"),

    ("01.4", "Chorvachilik", "Животноводство", "Animal production"),
    ("01.41", "Sut beruvchi yirik shoxli qoramol zotlarini boqish", "Разведение молочных пород крупного рогатого скота",
     "Raising of dairy cattle"),
    ("01.41.0", "Sut beruvchi yirik shoxli qoramol zotlarini boqish",
     "Разведение молочных пород крупного рогатого скота", "Raising of dairy cattle"),
    ("01.42", "Boshqa yirik shoxli qoramol zotlarini va buyvollarni boqish",
     "Разведение прочих пород крупного рогатого скота и буйволов", "Raising of other cattle and buffaloes"),
    ("01.42.0", "Boshqa yirik shoxli qoramol zotlarini va buyvollarni boqish",
     "Разведение прочих пород крупного рогатого скота и буйволов", "Raising of other cattle and buffaloes"),
    ("01.43", "Otlar va boshqa tuyoqli hayvonlarni boqish", "Разведение лошадей и прочих копытных пород",
     "Raising of horses and other equines"),
    ("01.43.1", "Otlar boqish", "Разведение лошадей", "Raising of horses"),
    ("01.43.2", "Eshaklar, xachirlar va boshqa tuyoqli hayvonlarni boqish",
     "Разведение ослов, мулов и лошаков и прочих копытных пород",
     "Raising of asses, mules and hinnies and other equines"),
    ("01.44", "Tuyalar va tuyaqoshlarni boqish", "Разведение верблюдов и верблюдовых",
     "Raising of camels and camelids"),
    ("01.44.0", "Tuyalar va tuyaqoshlarni boqish", "Разведение верблюдов и верблюдовых",
     "Raising of camels and camelids"),
    ("01.45", "Qo'y va echkilarni boqish", "Разведение овец и коз", "Raising of sheep and goats"),
    ("01.45.1", "Qorako'l zotli qo'ylarni boqish", "Разведение овец каракульских пород",
     "Raising of Karakul sheep breeds"),
    ("01.45.2", "Qorako'l zotlaridan tashqari qo'ylarni boqish", "Разведение овец, кроме каракульских пород",
     "Raising of sheep, except Karakul sheep breeds"),
    ("01.45.3", "Echkilarni boqish", "Разведение коз", "Raising of goats"),
    ("01.46", "Cho'chqa va cho'chqachalarni boqish", "Разведение свиней и поросят", "Raising of swine/pigs"),
    ("01.46.0", "Cho'chqa va cho'chqachalarni boqish", "Разведение свиней и поросят", "Raising of swine/pigs"),
    ("01.47", "Parrandachilik", "Птицеводство", "Raising of poultry"),
    ("01.47.0", "Parrandachilik", "Птицеводство", "Raising of poultry"),
    ("01.49", "Boshqa turdagi hayvonlarni boqish", "Разведение прочих видов животных", "Raising of other animals"),
    ("01.49.1", "Ipak qurtini boqish", "Разведение шелкопряда", "Raising of silkworms"),
    ("01.49.2", "Asalarichilik", "Разведение пчел", "Raising of bees"),
    ("01.49.3", "Quyonlarni va boshqa mo'ynali hayvonlarni boqish", "Разведение кроликов и прочих пушных зверей",
     "Raising of rabbits and other fur animals"),
    ("01.49.9", "Boshqa turdagi hayvonlarni boqish, boshqa toifaga kiritilmagan",
     "Разведение прочих животных, не включенных в другие категории",
     "Raising of other animals not elsewhere classified"),

    ("01.5", "Ardash qishloq xo'jaligi", "Смешанное сельское хозяйство", "Mixed farming"),
    ("01.50", "Ardash qishloq xo'jaligi", "Смешанное сельское хозяйство", "Mixed farming"),
    ("01.50.0", "Ardash qishloq xo'jaligi", "Смешанное сельское хозяйство", "Mixed farming"),

    ("01.6", "Qishloq xo'jaligi sohasidagi yordamchi faoliyatlar",
     "Вспомогательные виды деятельности в области сельского хозяйства",
     "Support activities for agriculture and post-harvest crop activities"),
    ("01.61", "Ekin yetishtirish sohasidagi yordamchi faoliyatlar",
     "Вспомогательные виды деятельности в области выращивания сельскохозяйственных культур",
     "Support activities for crop production"),
    ("01.61.1", "Operator va texnik xodimlar bilan birga qishloq xo'jaligi texnikasini taqdim etish",
     "Предоставление сельскохозяйственной техники вместе с оператором и техническим персоналом",
     "Provision of agricultural machinery with operator and technical personnel"),
    ("01.61.2", "Ekinlarni kasallik va zararkunandalardan, kemiruvchilardan himoya qilish",
     "Защита растений от болезней и насекомых-вредителей, а также грызунов",
     "Protection of plants against diseases and insect pests, as well as rodents"),
    ("01.61.3", "Qishloq xo'jaligi sug'orish uskunalariga xizmat ko'rsatish",
     "Обслуживание сельскохозяйственного поливного оборудования", "Servicing of agricultural irrigation equipment"),
    ("01.61.9", "Ekinchilik sohasidagi boshqa xizmatlarni ko'rsatish",
     "Предоставление прочих услуг в области растениеводства",
     "Provision of other services in the field of crop production"),
    ("01.62", "Hayvonlarni boqish bo'yicha yordamchi faoliyatlar",
     "Вспомогательные виды деятельности по разведению животных", "Support activities for animal production"),
    ("01.62.0", "Hayvonlarni boqish bo'yicha yordamchi faoliyatlar",
     "Вспомогательные виды деятельности по разведению животных", "Support activities for animal production"),
    ("01.63", "Hosildan keyingi qishloq xo'jaligi faoliyati", "Сельскохозяйственная деятельность после сбора урожая",
     "Post-harvest crop activities"),
    ("01.63.0", "Hosildan keyingi qishloq xo'jaligi faoliyati", "Сельскохозяйственная деятельность после сбора урожая",
     "Post-harvest crop activities"),
    ("01.64", "Ko'paytirish uchun urug'larni qayta ishlash va tayyorlash",
     "Обработка и подготовка семян для размножения", "Seed processing for propagation"),
    ("01.64.0", "Ko'paytirish uchun urug'larni qayta ishlash va tayyorlash",
     "Обработка и подготовка семян для размножения", "Seed processing for propagation"),

    ("01.7", "Yovvoyi hayvonlarni ovlash va tutish, shu jumladan ushbu sohalarda xizmat ko'rsatish",
     "Охота и отлов диких животных, включая предоставление услуг в этих областях",
     "Hunting, trapping and related service activities"),
    ("01.70", "Yovvoyi hayvonlarni ovlash va tutish, shu jumladan ushbu sohalarda xizmat ko'rsatish",
     "Охота и отлов диких животных, включая предоставление услуг в этих областях",
     "Hunting, trapping and related service activities"),
    ("01.70.0", "Yovvoyi hayvonlarni ovlash va tutish, shu jumladan ushbu sohalarda xizmat ko'rsatish",
     "Охота и отлов диких животных, включая предоставление услуг в этих областях",
     "Hunting, trapping and related service activities"),

    ("02", "O'RMONCHILIK VA O'RMON ZAGOTOFKASI", "ЛЕСОВОДСТВО И ЛЕСОЗАГОТОВКИ", "FORESTRY AND LOGGING"),
    ("02.1", "O'rmon xo'jaligi va boshqa o'rmon xo'jaligi faoliyati",
     "Лесоводство и прочая лесохозяйственная деятельность", "Silviculture and other forestry activities"),
    ("02.10", "O'rmon xo'jaligi va boshqa o'rmon xo'jaligi faoliyati",
     "Лесоводство и прочая лесохозяйственная деятельность", "Silviculture and other forestry activities"),
    ("02.10.0", "O'rmon xo'jaligi va boshqa o'rmon xo'jaligi faoliyati",
     "Лесоводство и прочая лесохозяйственная деятельность", "Silviculture and other forestry activities"),
    ("02.2", "O'rmon zagotovkasi", "Лесозаготовки", "Logging"),
    ("02.20", "O'rmon zagotovkasi", "Лесозаготовки", "Logging"),
    ("02.20.0", "O'rmon zagotovkasi", "Лесозаготовки", "Logging"),
    ("02.3", "Yog'ochdan bo'lmagan o'rmon mahsulotlarini yig'ish", "Сбор не древесных лесопродуктов",
     "Gathering of non-wood forest products"),
    ("02.30", "Yog'ochdan bo'lmagan o'rmon mahsulotlarini yig'ish", "Сбор не древесных лесопродуктов",
     "Gathering of non-wood forest products"),
    ("02.30.0", "Yog'ochdan bo'lmagan o'rmon mahsulotlarini yig'ish", "Сбор не древесных лесопродуктов",
     "Gathering of non-wood forest products"),
    ("02.4", "O'rmon xo'jaligi sohasidagi texnik xizmatlar", "Технические услуги в области лесоводства",
     "Support services for forestry"),
    ("02.40", "O'rmon xo'jaligi sohasidagi texnik xizmatlar", "Технические услуги в области лесоводства",
     "Support services for forestry"),
    ("02.40.0", "O'rmon xo'jaligi sohasidagi texnik xizmatlar", "Технические услуги в области лесоводства",
     "Support services for forestry"),

    ("03", "Baliqchilik va akvakultura", "РЫБОЛОВСТВО И АКВАКУЛЬТУРА", "FISHING AND AQUACULTURE"),
    ("03.1", "Baliqchilik", "Рыболовство", "Fishing"),
    ("03.11", "Dengiz baliqchiligi", "Морское рыболовство", "Marine fishing"),
    ("03.11.0", "Dengiz baliqchiligi", "Морское рыболовство", "Marine fishing"),
    ("03.12", "Chuchuk suv baliqchiligi", "Пресноводное рыболовство", "Freshwater fishing"),
    ("03.12.0", "Chuchuk suv baliqchiligi", "Пресноводное рыболовство", "Freshwater fishing"),
    ("03.2", "Akvakultura", "Аквакультура", "Aquaculture"),
    ("03.21", "Dengiz akvakulturasi", "Аквакультура морская", "Marine aquaculture"),
    ("03.21.0", "Dengiz akvakulturasi", "Аквакультура морская", "Marine aquaculture"),
    ("03.22", "Chuchuk suv akvakulturasi", "Аквакультура пресноводная", "Freshwater aquaculture"),
    ("03.22.0", "Chuchuk suv akvakulturasi", "Аквакультура пресноводная", "Freshwater aquaculture"),

    # SECTOR 2
    ("SECTOR_2", "Tog'-kon sanoati va karerlarni qazib olish", "ГОРНОДОБЫВАЮЩАЯ ПРОМЫШЛЕННОСТЬ И РАЗРАБОТКА КАРЬЕРОВ",
     "MINING AND QUARRYING"),

    ("05", "Ko'mir va lignit qazib olish", "ДОБЫЧА УГЛЯ И ЛИГНИТА", "MINING OF COAL AND LIGNITE"),
    ("05.1", "Toshko'mir qazib olish", "Добыча каменного угля", "Mining of hard coal"),
    ("05.10", "Toshko'mir qazib olish", "Добыча каменного угля", "Mining of hard coal"),
    ("05.10.0", "Toshko'mir qazib olish", "Добыча каменного угля", "Mining of hard coal"),
    ("05.2", "Lignit qazib olish", "Добыча лигнита", "Mining of lignite"),
    ("05.20", "Lignit qazib olish", "Добыча лигнита", "Mining of lignite"),
    ("05.20.0", "Lignit qazib olish", "Добыча лигнита", "Mining of lignite"),

    ("06", "Xom neft va tabiiy gaz qazib olish", "ДОБЫЧА СЫРОЙ НЕФТИ И ПРИРОДНОГО ГАЗА",
     "EXTRACTION OF CRUDE PETROLEUM AND NATURAL GAS"),
    ("06.1", "Xom neft qazib olish", "Добыча сырой нефти", "Extraction of crude petroleum"),
    ("06.10", "Xom neft qazib olish", "Добыча сырой нефти", "Extraction of crude petroleum"),
    ("06.10.0", "Xom neft qazib olish", "Добыча сырой нефти", "Extraction of crude petroleum"),
    ("06.2", "Tabiiy gaz qazib olish", "Добыча природного газа", "Extraction of natural gas"),
    ("06.20", "Tabiiy gaz qazib olish", "Добыча природного газа", "Extraction of natural gas"),
    ("06.20.0", "Tabiiy gaz qazib olish", "Добыча природного газа", "Extraction of natural gas"),

    ("07", "Metall rudalarini qazib olish", "ДОБЫЧА МЕТАЛЛИЧЕСКИХ РУД", "MINING OF METAL ORES"),
    ("07.1", "Temir rudasini qazib olish", "Добыча железной руды", "Mining of iron ores"),
    ("07.10", "Temir rudasini qazib olish", "Добыча железной руды", "Mining of iron ores"),
    ("07.10.0", "Temir rudasini qazib olish", "Добыча железной руды", "Mining of iron ores"),
    ("07.2", "Rangli metall rudalarini qazib olish", "Добыча руд цветных металлов", "Mining of non-ferrous metal ores"),
    ("07.21", "Uran va toriy rudasini qazib olish", "Добыча урановой и ториевой руды",
     "Mining of uranium and thorium ores"),
    ("07.21.0", "Uran va toriy rudasini qazib olish", "Добыча урановой и ториевой руды",
     "Mining of uranium and thorium ores"),
    ("07.29", "Boshqa rangli metall rudalarini qazib olish", "Добыча руд прочих цветных металлов",
     "Mining of other non-ferrous metal ores"),
    ("07.29.0", "Boshqa rangli metall rudalarini qazib olish", "Добыча руд прочих цветных металлов",
     "Mining of other non-ferrous metal ores"),

    ("08", "Tog'-kon sanoatining boshqa faoliyatlari", "ПРОЧАЯ ДЕЯТЕЛЬНОСТЬ ГОРНОДОБЫВАЮЩЕЙ ПРОМЫШЛЕННОСТИ",
     "OTHER MINING AND QUARRYING ACTIVITIES"),
    ("08.1", "Tosh, loy va qum karerlarini qazib olish", "Разработка каменных, глиняных и песчаных карьеров",
     "Quarrying of stone, clay and sand"),
    ("08.11", "Pardozlash va qurilish toshi, ohaktosh, gips, bo'r va slanets qazib olish",
     "Добыча отделочного и строительного камня, известняка, гипса, мела и сланцев",
     "Quarrying of ornamental and building stone, limestone, gypsum, chalk and slate"),
    ("08.11.0", "Pardozlash va qurilish toshi, ohaktosh, gips, bo'r va slanets qazib olish",
     "Добыча отделочного и строительного камня, известняка, гипса, мела и сланцев",
     "Quarrying of ornamental and building stone, limestone, gypsum, chalk and slate"),
    ("08.12", "Shag'al va qum karerlarini qazib olish, loy va kaolin qazib olish",
     "Разработка гравийных и песчаных карьеров, добыча глины и каолина",
     "Operation of gravel and sand pits; mining of clays and kaolin"),
    ("08.12.0", "Shag'al va qum karerlarini qazib olish", "Разработка гравийных и песчаных карьеров",
     "Operation of gravel and sand pits"),
    ("08.12.1", "Loy va kaolin qazib olish", "Добыча глины и каолина", "Mining of clay and kaolin"),
    ("08.12.2", "Kaolin va boshqa kaolin loylarini boyitish va birlamchi qayta ishlash",
     "Обогащение и аналогичная первичная обработка каолина и глин каолиновых прочих",
     "Beneficiation and similar primary processing of kaolin and other kaolin clays"),
    ("08.12.9", "Boshqa karerlarni qazib olish, boshqa toifaga kiritilmagan",
     "Разработка прочих карьеров, не включенных в другие категории",
     "Quarrying of other quarries not elsewhere classified"),
    ("08.9", "Boshqa tog'-kon sanoati faoliyatlari, boshqa toifaga kiritilmagan",
     "Деятельность горнодобывающей промышленности и разработка карьеров, не включенные в другие категории",
     "Other mining and quarrying activities not elsewhere classified"),
    ("08.91", "Kimyo sanoati va o'g'it ishlab chiqarish uchun mineral xomashyo qazib olish",
     "Добыча минерального сырья для химической промышленности и производства удобрений",
     "Mining of chemical and fertiliser minerals"),
    ("08.91.0", "Kimyo sanoati va o'g'it ishlab chiqarish uchun mineral xomashyo qazib olish",
     "Добыча минерального сырья для химической промышленности и производства удобрений",
     "Mining of chemical and fertiliser minerals"),
    ("08.92", "Torfdan foydalanish", "Добыча торфа", "Extraction of peat"),
    ("08.92.0", "Torfdan foydalanish", "Добыча торфа", "Extraction of peat"),
    ("08.93", "Tuz qazib olish", "Добыча соли", "Extraction of salt"),
    ("08.93.0", "Tuz qazib olish", "Добыча соли", "Extraction of salt"),
    ("08.99", "Boshqa tog'-kon sanoati faoliyatlari, boshqa toifaga kiritilmagan",
     "Деятельность горнодобывающей промышленности, не включенной в другие категории",
     "Other mining and quarrying activities not elsewhere classified"),
    ("08.99.0", "Boshqa tog'-kon sanoati faoliyatlari, boshqa toifaga kiritilmagan",
     "Деятельность горнодобывающей промышленности, не включенной в другие категории",
     "Other mining and quarrying activities not elsewhere classified"),

    ("09", "Tog'-kon sanoatida texnik xizmatlar", "Технические услуги в области горнодобывающей промышленности",
     "Support activities for mining and quarrying"),
    ("09.1", "Neft va tabiiy gaz qazib olish sohasidagi texnik xizmatlar",
     "Технические услуги в области добычи нефти и природного газа",
     "Support activities for petroleum and natural gas mining"),
    ("09.10", "Neft va tabiiy gaz qazib olish sohasidagi texnik xizmatlar",
     "Технические услуги в области добычи нефти и природного газа",
     "Support activities for petroleum and natural gas mining"),
    ("09.10.0", "Neft va tabiiy gaz qazib olish sohasidagi texnik xizmatlar",
     "Технические услуги в области добычи нефти и природного газа",
     "Support activities for petroleum and natural gas mining"),
    ("09.9", "Tog'-kon sanoatining boshqa sohalarida texnik yordam va yer osti ishlari",
     "Техническая поддержка для прочих областей горнодобывающей промышленности и подземной разработки",
     "Support activities for other mining and quarrying"),
    ("09.90", "Tog'-kon sanoatining boshqa sohalarida texnik yordam va yer osti ishlari",
     "Техническая поддержка для прочих областей горнодобывающей промышленности и подземной разработки",
     "Support activities for other mining and quarrying"),
    ("09.90.0", "Tog'-kon sanoatining boshqa sohalarida texnik yordam va yer osti ishlari",
     "Техническая поддержка для прочих областей горнодобывающей промышленности и подземной разработки",
     "Support activities for other mining and quarrying"),

    # SECTOR 3
    ("SECTOR_3", "ISHLAB CHIQARISH KORXONALARI", "ПРОИЗВОДСТВСТВЕННЫЕ ПРЕДПРИЯТИЯ", "MANUFACTURING"),

    ("10", "Oziq-ovqat mahsulotlari ishlab chiqarish", "ПРОИЗВОДСТВО ПРОДУКТОВ ПИТАНИЯ",
     "MANUFACTURE OF FOOD PRODUCTS"),
    ("10.1", "Go'shtni qayta ishlash va konservalash, go'sht mahsulotlari ishlab chiqarish",
     "Переработка и консервирование мяса, производство мясных изделий",
     "Processing and preserving of meat and manufacture of meat products"),
    ("10.11", "Go'shtni qayta ishlash", "Переработка мяса", "Processing of meat"),
    ("10.11.1", "So'yish, go'shtni qayta ishlash yoki qadoqlash",
     "Забой скота на скотобойне, обработка или расфасовка мяса",
     "Slaughtering of animals on a slaughterhouse, processing or packaging of meat"),
    ("10.11.2", "Yangi, sovutilgan yoki muzlatilgan go'sht ishlab chiqarish",
     "Производство свежего, охлажденного или замороженного мяса", "Production of fresh, chilled or frozen meat"),
    ("10.11.9", "Go'shtni qayta ishlash bo'yicha boshqa faoliyatlar", "Прочая деятельность по переработке мяса",
     "Other meat processing activities"),
    ("10.12", "Parranda go'shtini qayta ishlash", "Переработка мяса домашней птицы", "Processing of poultry meat"),
    ("10.12.0", "Parranda go'shtini qayta ishlash", "Переработка мяса домашней птицы", "Processing of poultry meat"),
    ("10.13", "Go'sht va parranda go'shtidan mahsulotlar ishlab chiqarish",
     "Производство продуктов из мяса и мяса домашней птицы", "Manufacture of meat and poultry meat products"),
    ("10.13.1",
     "Tuzlangan, marinadlangan, quritilgan yoki dudlangan go'sht, parranda go'shti va oziqaviy submahsulotlar ishlab chiqarish",
     "Производство соленых, в рассоле, сушеных или копченых мяса, мяса птицы и пищевых субпродуктов",
     "Manufacture of salted, in brine, dried or smoked meat, poultry meat and edible offal"),
    ("10.13.2", "Kolbasa mahsulotlari ishlab chiqarish", "Производство колбасных изделий",
     "Manufacture of sausages and similar products"),
    ("10.13.9", "Boshqa toifaga kiritilmagan boshqa go'sht mahsulotlari ishlab chiqarish",
     "Производство прочих мясных продуктов, не включенных в другие категории",
     "Manufacture of other meat products not elsewhere classified"),

    ("10.2", "Baliq, qisqichbaqasimonlar va mollyuskalarni qayta ishlash va konservalash",
     "Переработка и консервирование рыбы, ракообразных и моллюсков",
     "Processing and preserving of fish, crustaceans and molluscs"),
    ("10.20", "Baliq, qisqichbaqasimonlar va mollyuskalarni qayta ishlash va konservalash",
     "Переработка и консервирование рыбы, ракообразных и моллюсков",
     "Processing and preserving of fish, crustaceans and molluscs"),
    ("10.20.0", "Baliq, qisqichbaqasimonlar va mollyuskalarni qayta ishlash va konservalash",
     "Переработка и консервирование рыбы, ракообразных и моллюсков",
     "Processing and preserving of fish, crustaceans and molluscs"),

    ("10.3", "Meva va sabzavotlarni qayta ishlash va konservalash", "Переработка и консервирование фруктов и овощей",
     "Processing and preserving of fruit and vegetables"),
    ("10.31", "Kartoshkani qayta ishlash va konservalash", "Переработка и консервирование картофеля",
     "Processing and preserving of potatoes"),
    ("10.31.0", "Kartoshkani qayta ishlash va konservalash", "Переработка и консервирование картофеля",
     "Processing and preserving of potatoes"),
    ("10.32", "Meva va sabzavot sharbatlarini ishlab chiqarish", "Производство фруктовых и овощных соков",
     "Manufacture of fruit and vegetable juice"),
    ("10.32.0", "Meva va sabzavot sharbatlarini ishlab chiqarish", "Производство фруктовых и овощных соков",
     "Manufacture of fruit and vegetable juice"),
    ("10.39", "Meva va sabzavotlarni boshqa turda qayta ishlash va konservalash",
     "Прочие виды переработки и консервирования фруктов и овощей",
     "Other processing and preserving of fruit and vegetables"),
    ("10.39.0", "Meva va sabzavotlarni boshqa turda qayta ishlash va konservalash",
     "Прочие виды переработки и консервирования фруктов и овощей",
     "Other processing and preserving of fruit and vegetables"),

    ("10.4", "O'simlik va hayvon yog'lari va yog'larini ishlab chiqarish",
     "Производство растительных и животных масел и жиров", "Manufacture of vegetable and animal oils and fats"),
    ("10.41", "O'simlik va hayvon yog'lari va yog'larini ishlab chiqarish",
     "Производство растительных и животных масел и жиров", "Manufacture of crude vegetable and animal oils and fats"),
    ("10.41.0", "O'simlik va hayvon yog'lari va yog'larini ishlab chiqarish",
     "Производство растительных и животных масел и жиров", "Manufacture of crude vegetable and animal oils and fats"),
    ("10.42", "Margarina va aralash oziq-ovqat yog'larini ishlab chiqarish",
     "Производство маргарина и смешанных пищевых жиров", "Manufacture of margarine and similar edible fats"),
    ("10.42.0", "Margarina va aralash oziq-ovqat yog'larini ishlab chiqarish",
     "Производство маргарина и смешанных пищевых жиров", "Manufacture of margarine and similar edible fats"),

    ("10.5", "Sut mahsulotlari ishlab chiqarish", "Производство молочных продуктов", "Manufacture of dairy products"),
    ("10.51", "Sutni qayta ishlash va pishloq ishlab chiqarish", "Переработка молока и производство сыра",
     "Operation of dairies and cheese making"),
    ("10.51.0", "Sutni qayta ishlash va pishloq ishlab chiqarish", "Переработка молока и производство сыра",
     "Operation of dairies and cheese making"),
    ("10.52", "Muzqaymoq ishlab chiqarish", "Производство мороженого", "Manufacture of ice cream"),
    ("10.52.0", "Muzqaymoq ishlab chiqarish", "Производство мороженого", "Manufacture of ice cream"),

    ("10.6", "Un, kraxmal va kraxmal mahsulotlari ishlab chiqarish",
     "Производство продуктов мукомольной промышленности, крахмалов и крахмальных продуктов",
     "Manufacture of grain mill products, starches and starch products"),
    ("10.61", "Un-yorma mahsulotlari ishlab chiqarish", "Производство продуктов мукомольно-крупяной промышленности",
     "Manufacture of grain mill products"),
    ("10.61.0", "Un-yorma mahsulotlari ishlab chiqarish", "Производство продуктов мукомольно-крупяной промышленности",
     "Manufacture of grain mill products"),
    ("10.62", "Kraxmal va kraxmalli mahsulotlar ishlab chiqarish", "Производство крахмала и продукции из крахмала",
     "Manufacture of starches and starch products"),
    ("10.62.0", "Kraxmal va kraxmalli mahsulotlar ishlab chiqarish", "Производство крахмала и продукции из крахмала",
     "Manufacture of starches and starch products"),

    ("10.7", "Non, qandolat va un mahsulotlari ishlab chiqarish", "Производство хлебобулочных и мучных изделий",
     "Manufacture of bread; manufacture of fresh pastry goods and cakes"),
    ("10.71", "Non, yangi unli qandolat, tort va piroglar ishlab chiqarish",
     "Производство хлеба, свежих мучных кондитерских изделий, тортов и пирожных",
     "Manufacture of bread; manufacture of fresh pastry goods and cakes"),
    ("10.71.0", "Non, yangi unli qandolat, tort va piroglar ishlab chiqarish",
     "Производство хлеба, свежих мучных кондитерских изделий, тортов и пирожных",
     "Manufacture of bread; manufacture of fresh pastry goods and cakes"),
    ("10.72", "Suxari, pechenye, uzoq saqlanadigan unli qandolat mahsulotlari ishlab chiqarish",
     "Производство сухарей и печенья, мучных кондитерских изделий длительного хранения",
     "Manufacture of rusks and biscuits; manufacture of preserved pastry goods and cakes"),
    ("10.72.0", "Suxari, pechenye, uzoq saqlanadigan unli qandolat mahsulotlari ishlab chiqarish",
     "Производство сухарей и печенья, мучных кондитерских изделий длительного хранения",
     "Manufacture of rusks and biscuits; manufacture of preserved pastry goods and cakes"),
    ("10.73", "Makaron mahsulotlari va shunga o'xshash un mahsulotlari ishlab chiqarish",
     "Производство макаронных изделий и аналогичных мучных продуктов",
     "Manufacture of macaroni, noodles, couscous and similar farinaceous products"),
    ("10.73.0", "Makaron mahsulotlari va shunga o'xshash un mahsulotlari ishlab chiqarish",
     "Производство макаронных изделий и аналогичных мучных продуктов",
     "Manufacture of macaroni, noodles, couscous and similar farinaceous products"),

    ("10.8", "Boshqa oziq-ovqat mahsulotlari ishlab chiqarish", "Производство прочих продуктов питания",
     "Manufacture of other food products"),
    ("10.81", "Shakar ishlab chiqarish", "Производство сахара", "Manufacture of sugar"),
    ("10.81.0", "Shakar ishlab chiqarish", "Производство сахара", "Manufacture of sugar"),
    ("10.82", "Kakao, shokolad va shakarli qandolat mahsulotlari ishlab chiqarish",
     "Производство какао, шоколада и сахаристых кондитерских изделий",
     "Manufacture of cocoa, chocolate and sugar confectionery"),
    ("10.82.0", "Kakao, shokolad va shakarli qandolat mahsulotlari ishlab chiqarish",
     "Производство какао, шоколада и сахаристых кондитерских изделий",
     "Manufacture of cocoa, chocolate and sugar confectionery"),
    ("10.83", "Choy va kofeni qayta ishlash", "Переработка чая и кофе", "Processing of tea and coffee"),
    ("10.83.0", "Choy va kofeni qayta ishlash", "Переработка чая и кофе", "Processing of tea and coffee"),
    ("10.84", "Ziravorlar va qo'shimchalar ishlab chiqarish", "Производство пряностей и приправ",
     "Manufacture of spices and condiments"),
    ("10.84.0", "Ziravorlar va qo'shimchalar ishlab chiqarish", "Производство пряностей и приправ",
     "Manufacture of spices and condiments"),
    ("10.85", "Tayyor oziq-ovqat mahsulotlari ishlab chiqarish", "Производство готовых пищевых продуктов",
     "Manufacture of prepared meals and dishes"),
    ("10.85.0", "Tayyor oziq-ovqat mahsulotlari ishlab chiqarish", "Производство готовых пищевых продуктов",
     "Manufacture of prepared meals and dishes"),
    ("10.86", "Bolalar ovqatlari va parhez oziq-ovqat mahsulotlari ishlab chiqarish",
     "Производство детского питания и диетических пищевых продуктов",
     "Manufacture of homogenised food preparations and dietetic food"),
    ("10.86.0", "Bolalar ovqatlari va parhez oziq-ovqat mahsulotlari ishlab chiqarish",
     "Производство детского питания и диетических пищевых продуктов",
     "Manufacture of homogenised food preparations and dietetic food"),
    ("10.89", "Boshqa toifaga kiritilmagan boshqa oziq-ovqat mahsulotlari ishlab chiqarish",
     "Производство прочих продуктов питания, не включенных в другие категории",
     "Manufacture of other food products not elsewhere classified"),
    ("10.89.0", "Boshqa toifaga kiritilmagan boshqa oziq-ovqat mahsulotlari ishlab chiqarish",
     "Производство прочих продуктов питания, не включенных в другие категории",
     "Manufacture of other food products not elsewhere classified"),

    ("10.9", "Hayvonlar uchun tayyor ozuqalar ishlab chiqarish", "Производство готовых кормов для животных",
     "Manufacture of prepared animal feeds"),
    ("10.91", "Fermada boqiladigan hayvonlar uchun tayyor ozuqalar ishlab chiqarish",
     "Производство готовых кормов для животных, содержащихся на фермах",
     "Manufacture of prepared feeds for farm animals"),
    ("10.91.0", "Fermada boqiladigan hayvonlar uchun tayyor ozuqalar ishlab chiqarish",
     "Производство готовых кормов для животных, содержащихся на фермах",
     "Manufacture of prepared feeds for farm animals"),
    ("10.92", "Uy hayvonlari uchun tayyor ozuqalar ishlab chiqarish",
     "Производство готовых кормов для домашних животных", "Manufacture of prepared pet foods"),
    ("10.92.0", "Uy hayvonlari uchun tayyor ozuqalar ishlab chiqarish",
     "Производство готовых кормов для домашних животных", "Manufacture of prepared pet foods"),

    ("11", "Ichimliklar ishlab chiqarish", "ПРОИЗВОДСТВО НАПИТКОВ", "MANUFACTURE OF BEVERAGES"),
    ("11.0", "Ichimliklar ishlab chiqarish", "Производство напитков", "Manufacture of beverages"),
    ("11.01", "Spirtli ichimliklarni distillash, rektifikatsiya va aralashtirish",
     "Дистилляция, ректификация и смешивание спиртных напитков", "Distilling, rectifying and blending of spirits"),
    ("11.01.0", "Spirtli ichimliklarni distillash, rektifikatsiya va aralashtirish",
     "Дистилляция, ректификация и смешивание спиртных напитков", "Distilling, rectifying and blending of spirits"),
    ("11.02", "Uzumdan sharob ishlab chiqarish", "Производство вина из винограда", "Manufacture of wine from grapes"),
    ("11.02.0", "Uzumdan sharob ishlab chiqarish", "Производство вина из винограда", "Manufacture of wine from grapes"),
    ("11.03", "Sidr va boshqa mevali vinolar ishlab chiqarish", "Производство сидра и прочих фруктовых вин",
     "Manufacture of cider and other fruit wines"),
    ("11.03.0", "Sidr va boshqa mevali vinolar ishlab chiqarish", "Производство сидра и прочих фруктовых вин",
     "Manufacture of cider and other fruit wines"),
    ("11.04", "Boshqa distillanmagan fermentlangan ichimliklar ishlab chiqarish",
     "Производство прочих недистиллированных ферментированных напитков",
     "Manufacture of other non-distilled fermented beverages"),
    ("11.04.0", "Boshqa distillanmagan fermentlangan ichimliklar ishlab chiqarish",
     "Производство прочих недистиллированных ферментированных напитков",
     "Manufacture of other non-distilled fermented beverages"),
    ("11.05", "Pivo ishlab chiqarish", "Производство пива", "Manufacture of beer"),
    ("11.05.0", "Pivo ishlab chiqarish", "Производство пива", "Manufacture of beer"),
    ("11.06", "Solod ishlab chiqarish", "Производство солода", "Manufacture of malt"),
    ("11.06.0", "Solod ishlab chiqarish", "Производство солода", "Manufacture of malt"),
    ("11.07", "Alkogolsiz ichimliklar ishlab chiqarish; mineral suvlar va shishadagi boshqa suvlarni ishlab chiqarish",
     "Производство безалкогольных напитков; производство минеральных вод и других вод в бутылках",
     "Manufacture of soft drinks; production of mineral waters and other bottled waters"),
    ("11.07.0",
     "Alkogolsiz ichimliklar ishlab chiqarish; mineral suvlar va shishadagi boshqa suvlarni ishlab chiqarish",
     "Производство безалкогольных напитков; производство минеральных вод и других вод в бутылках",
     "Manufacture of soft drinks; production of mineral waters and other bottled waters"),

    ("12", "Tamaki mahsulotlari ishlab chiqarish", "ПРОИЗВОДСТВО ТАБАЧНЫХ ИЗДЕЛИЙ", "MANUFACTURE OF TOBACCO PRODUCTS"),
    ("12.0", "Tamaki mahsulotlari ishlab chiqarish", "Производство табачных изделий",
     "Manufacture of tobacco products"),
    ("12.00", "Tamaki mahsulotlari ishlab chiqarish", "Производство табачных изделий",
     "Manufacture of tobacco products"),
    ("12.00.0", "Tamaki mahsulotlari ishlab chiqarish", "Производство табачных изделий",
     "Manufacture of tobacco products"),

    # ... Boshqa sektorlar (33-gacha davom etadi)
]


def get_level_from_code(code):
    """Kodga asoslanib darajani aniqlaydi (OKED standartiga qat'iy amal qilgan holda)."""
    if code.startswith("SECTOR_"):
        return 1

    parts = code.split('.')
    num_dots = code.count('.')

    if num_dots == 0:
        # Kod: 01, 10, 11 kabi (Razdel)
        return 2

    # Agar nuqtalar soni 1 bo'lsa (01.1 yoki 01.11, 10.1, 10.11):
    if num_dots == 1:
        # Kod: 01.1, 10.1, 11.0 kabi (Gruppa) -> Level 3
        # Kod: 01.11, 10.11 kabi (Klass) -> Level 4
        if len(parts[-1]) == 1:
            return 3
        elif len(parts[-1]) == 2:
            return 4

    # Agar nuqtalar soni 2 bo'lsa (01.11.1, 10.11.1 kabi) (Podklass)
    if num_dots == 2:
        return 5

    return 6  # Boshqa holatlar (agar mavjud bo'lsa)


def get_parent_code_from_code(code):
    """Kodga asoslanib ota kategoriyaning kodini aniqlaydi (prefiksni kesish orqali)."""
    if code.startswith("SECTOR_"):
        return None

    # Razdel (XX) uchun ota SECTOR_X ni topish
    parts = code.split('.')
    if len(parts) == 1:
        try:
            razdel_num = int(code)
            # Sektorlarni aniqlash (Men faqat PDFdagi ma'lumotlarga asoslanaman)
            if 1 <= razdel_num <= 3: return "SECTOR_1"
            if 5 <= razdel_num <= 9: return "SECTOR_2"
            if 10 <= razdel_num <= 33: return "SECTOR_3"
            # va hokazo.
            return "SECTOR_?"
        except ValueError:
            return None

            # 01.11.1 -> 01.11
    # 01.11 -> 01.1
    # 01.1 -> 01
    parent_code = ".".join(parts[:-1])

    return parent_code


def import_oked_categories_final_v2():
    """
    Oldindan tayyorlangan OKED ma'lumotlarini (3 tilda)
    CategoryModelga qat'iy ierarxik saqlash funksiyasi (prefiksga asoslangan).
    """

    # Saqlangan obyektlarni kod orqali tez topish uchun
    category_map = {}

    print("Tayyorlangan OKED kategoriyalarining importi boshlandi (Final v2)...")

    try:
        with transaction.atomic():

            # 1. Barcha kategoriyalarni yaratish
            for code, name_uz, name_ru, name_en in OKED_TRIPLE_CATEGORIES:

                # --- Ota-kategoriyani topish ---
                parent_code = get_parent_code_from_code(code)
                parent_obj = category_map.get(parent_code)

                # --- IKKILANISHNI TEKSHIRISH (Nom takrorlansa pastki darajani o'tkazib yuborish) ---
                if parent_obj and parent_obj.name == name_uz and get_level_from_code(code) > get_level_from_code(
                        parent_code):
                    print(
                        f"O'tkazib yuborildi: '{name_uz}' (Kod: {code}) - Ota ('{parent_obj.name}'/{parent_obj.code}) bilan bir xil nomga ega.")
                    continue

                # --- Levelni aniqlash ---
                level = get_level_from_code(code)

                # 2. Saqlash
                try:
                    # Agar ota obyekt topilsa, uning is_leaf'ini False qilish
                    if parent_obj and parent_obj.is_leaf:
                        parent_obj.is_leaf = False
                        parent_obj.save(update_fields=['is_leaf'])

                    category, created = CategoryModel.objects.get_or_create(
                        code=code,
                        defaults={
                            'name': name_uz,
                            'name_ru': name_ru,
                            'name_en': name_en,
                            'parent': parent_obj,
                            'level': level,
                            'is_leaf': True,
                        }
                    )

                    if created:
                        print(f"Yaratildi: {category.name} (Daraja: {level}, Kod: {category.code})")
                    else:
                        # Agar allaqachon yaratilgan bo'lsa, ma'lumotlarni yangilash
                        CategoryModel.objects.filter(code=code).update(
                            name=name_uz,
                            name_ru=name_ru,
                            name_en=name_en,
                            parent=parent_obj,
                            level=level
                        )
                        category = CategoryModel.objects.get(code=code)
                        print(f"Yangilandi: {category.name} (Kod: {category.code})")

                    # Joriy obyektni category_map'ga saqlash
                    category_map[code] = category

                except Exception as e:
                    print(f"Kategoriyani saqlashda xato: {name_uz} (Kod: {code}) -> {e}")
                    raise

        print("Kategoriyalar importi muvaffaqiyatli yakunlandi!")

    except Exception as e:
        print(f"Global xato: Kategoriyalar importi bekor qilindi. Xato: {e}")


###########################################
#
#       Davlatlarni qo'shadigan funksiya
#
###########################################


import pycountry
from core.apps.accounts.models.region import Country


def load_all_country_codes():
    """
    Barcha davlatlarning alpha-2 kodlarini ('UZ', 'RU', 'US', ...) name field ga yozadi.
    """
    for c in pycountry.countries:
        code = c.alpha_2.upper()  # KATTA HARFDA
        Country.objects.get_or_create(name=code)


from core.apps.main.models import PriceCountryModel
from core.apps.accounts.models.region import Country


def set_country_prices(default_price, custom_prices=None):
    """
    default_price -> ko‘pchilik davlatlar uchun narx
    custom_prices -> {"UZ": 10000, "RU": 20000} kabi alohida narxlar
    """

    if custom_prices is None:
        custom_prices = {}

    # Barcha davlatlarni olish
    all_countries = Country.objects.all()

    for country in all_countries:
        # Agar bu davlat custom bo'lsa — alohida narx
        price_value = custom_prices.get(country.name, default_price)

        PriceCountryModel.objects.update_or_create(
            country=country,
            defaults={"price": price_value}
        )


from core.apps.accounts.models.tg_ids import UserTgIds


def create_user_ids(count: int, user_ids):
    for _ in range(count):
        created = UserTgIds.objects.create(tg_id=user_ids)
        print(f"yaratildi:{_} {created.id}")

    return True
