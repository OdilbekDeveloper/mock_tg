from functions.user_data import get_user_data
import json
from functions.get_lang import get_lang
home_support = "❗️Diqqat siz qo'llab quvvatlash mutaxasisi🧑‍💻 bilan bog'lanmoqchisiz.\n\n☑️Suhbat davomida operator sizdan shaxsiy ma'lumotlarni so'rashi va undan foydalanishi mumkin. Bu holat sizning balansingizga ta'sir etmaydi"
home_support_ru = "❗️Внимание, вы хотите обратиться к специалисту службы поддержки🧑‍💻.\n\n☑️В ходе разговора оператор может запросить и использовать у вас личную информацию. Это не повлияет на ваш баланс"
home_support_eng = "❗️Attention, you are about to contact a support specialist🧑‍💻.\n\n☑️During the conversation, the operator may ask and use personal information from you. This will not affect your balance"
home_cabinet_edit = "Yangi ismingizni kiriting📝\n\nMisol uchun: Teshavoy"

add_money = "Kechirasiz🥲 bu bo'lim hozircha ta'mirda♻️"


def home_cabinet(telegram_id):
    lang = get_lang(telegram_id)
    user_data = get_user_data(telegram_id)
    data = json.loads(user_data)

    if lang == 'uz':
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        phone = data['phone']
        balance = data['balance']
        date_joined = data['date_joined']

        home_cabinet_data = (
            f"🆔ID: {telegram_id}\n"
            f"👤Ism familiya: {first_name} {last_name}\n"
            f"🌀Username: @{username}\n"
            f"📞Telefon raqam: {phone}\n"
            f"💰Balans: {balance} so'm\n"
            f"\n📅Ro'yhatdan o'tgan sana: {date_joined}"
        )
        return home_cabinet_data
    elif lang == 'ru':
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        phone = data['phone']
        balance = data['balance']
        date_joined = data['date_joined']
        
        home_cabinet_data = (
            f"🆔ИД: {telegram_id}\n"
            f"👤Имя и фамилия: {first_name} {last_name}\n"
            f"🌀Имя пользователя: @{username}\n"
            f"📞Номер телефона: {phone}\n"
            f"💰Баланс: {balance} сум\n"
            f"\n📅Дата регистрации: {date_joined}"
        )
        return home_cabinet_data

    elif lang == 'eng':
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        phone = data['phone']
        balance = data['balance']
        date_joined = data['date_joined']
        
        home_cabinet_data = (
            f"🆔ID: {telegram_id}\n"
            f"👤Fullname: {first_name} {last_name}\n"
            f"🌀Username: @{username}\n"
            f"📞Mobile number: {phone}\n"
            f"💰Balance: {balance} sum\n"
            f"\n📅Sign-up date: {date_joined}"
        )
        return home_cabinet_data



error_uz = "Kichik nosozlik. Adminga xabar bering!"
error_ru = "Небольшой сбой. Сообщить администратору"
error_eng = "Minor bug. Report to Admin!"


rules_eng = """Rules for IELTS Plus bot

Guidelines Access: Detailed guidelines are available through the Help button in the main menu. These guidelines cover various aspects, including test procedures, conduct, and support information.

Test Submission Requirement: Ensure that all answers are submitted before the test concludes. Unsubmitted answers at the test's end will not be saved in our database. To maintain fairness and integrity, refrain from engaging in any form of cheating or using unauthorized aids during the tests.

Reporting Issues: If encountering any issues or requiring assistance during the test, users are encouraged to utilize the dedicated report button available in the Help menu. Reporting problems promptly allows us to address concerns efficiently and enhance the user experience.

Material Sharing Policy: Sharing any test-related materials provided during the tests, including content from the speaking test, is strictly prohibited. However, users are permitted to share their test results and experiences with friends and peers.

Test Integrity and System Usage: Users are advised against refreshing the test interface or attempting to manipulate the system once the test has commenced. Any attempts to disrupt or misuse the test interface might lead to a temporary or permanent ban from accessing the services provided by the Telegram bot.

Respect for Others: Maintain a respectful and considerate attitude towards other users within the bot's community. Avoid engaging in any behavior that may disturb or inconvenience other test-takers.

Data Privacy and Security: The bot prioritizes user data privacy and security. Personal information provided during the test will be handled in accordance with our privacy policy, ensuring confidentiality and compliance with data protection regulations.

By adhering to these rules, users contribute to a fair, secure, and enriching testing environment for all participants accessing IELTS mock tests through the Telegram bot.


"""

rules_uz = """IELTS Plus bot qoidalari

Qo'llanmalar: Batafsil barcha video qo'llanmalarga kirish uchun asosiy menyudan Yordam tugmasini bosing. Ushbu qo'llanmalarda test jarayonidagi harakatlar va tavsiyalar berilgan.

Test topshirish talabi: Test topshirayotgan paytda berilgan vaqtdan biroz oldin barcha javoblarni kiritganligingizga ishonch hosil qiling. Audio tugagandan keyingi yoki berilgan vaqt tugaganidan keyingi javoblar ma'lumotlar bazasida saqlab qolinmaydi. Bu bizga test jarayoni adolatli va shaffof bo'lishiga yordam beradi.

Shikoyatlar yuborish: Bot ishlatish paytida qandaydir muammoga duch kelsangiz Yordam menyusi orqali bizga o'z muammoyingizni yozib qoldiring. 

Materiallarni tarqatish huquqi: Hech qaysi foydalanuvchi test davomida(og'zaki test ham) berilgan har qanday materialni tarqatishga haqqi yo'q. Aks holda foydalanuvchi botdan bloklanadi va hisobi muzlatiladi. 

Sinovning yaxlitligi va tizimdan foydalanish: Foydalanuvchilarga test boshlanganidan keyin test interfeysini yangilash yoki tizimni boshqarishga urinmaslik tavsiya etiladi. Test interfeysini buzish yoki noto‘g‘ri foydalanishga qaratilgan har qanday urinishlar Telegram bot tomonidan taqdim etilgan xizmatlarga kirishni vaqtincha yoki doimiy ravishda taqiqlashga olib kelishi mumkin.

Boshqalarga hurmat: Bot hamjamiyatidagi boshqa foydalanuvchilarga hurmatli va muloyim munosabatda bo'ling. Boshqa imtihon topshiruvchilarni bezovta qiladigan xatti-harakatlardan saqlaning.

Ma'lumotlarning maxfiyligi va xavfsizligi: Bot foydalanuvchi ma'lumotlarining maxfiyligi va xavfsizligini birinchi o'ringa qo'yadi. Sinov paytida taqdim etilgan shaxsiy ma'lumotlar bizning maxfiylik siyosatimizga muvofiq, maxfiylik va ma'lumotlarni himoya qilish qoidalariga rioya qilishni ta'minlaydi.


Ushbu qoidalarga rioya qilgan holda, foydalanuvchilar Telegram bot orqali IELTS mock testga kiradigan barcha ishtirokchilar uchun adolatli, xavfsiz va boyituvchi test muhitiga hissa qo‘shadilar.

"""

rules_ru = """
Правила IELTS Plus Bot

Доступ к рекомендациям: подробные рекомендации доступны через кнопку «Справка» в главном меню. Эти рекомендации охватывают различные аспекты, включая процедуры тестирования, поведение и вспомогательную информацию.

Требование к отправке теста: убедитесь, что все ответы отправлены до завершения теста. Неотправленные ответы по окончании теста не будут сохранены в нашей базе данных. Чтобы обеспечить справедливость и честность, воздерживайтесь от любых форм мошенничества или использования несанкционированных вспомогательных средств во время тестов.

Отчеты о проблемах. При возникновении каких-либо проблем или необходимости помощи во время теста пользователям рекомендуется использовать специальную кнопку отчета, доступную в меню «Справка». Своевременное сообщение о проблемах позволяет нам эффективно решать проблемы и улучшать качество обслуживания пользователей.

Политика обмена материалами: Распространение любых материалов, связанных с тестом, предоставленных во время тестов, включая материалы устного теста, строго запрещено. Тем не менее, пользователям разрешено делиться результатами своих тестов и опытом с друзьями и коллегами.

Тестирование целостности и использование системы. Пользователям не рекомендуется обновлять интерфейс теста или пытаться манипулировать системой после начала теста. Любые попытки нарушить работу тестового интерфейса или использовать его не по назначению могут привести к временному или постоянному запрету доступа к сервисам, предоставляемым ботом Telegram.

Уважение к другим: поддерживайте уважительное и внимательное отношение к другим пользователям в сообществе бота. Избегайте любого поведения, которое может беспокоить или доставлять неудобства другим участникам тестирования.

Конфиденциальность и безопасность данных: бот уделяет приоритетное внимание конфиденциальности и безопасности пользовательских данных. Личная информация, предоставленная во время теста, будет обрабатываться в соответствии с нашей политикой конфиденциальности, обеспечивая конфиденциальность и соблюдение правил защиты данных.

Соблюдая эти правила, пользователи способствуют созданию справедливой, безопасной и обогащающей среды тестирования для всех участников, получающих доступ к пробным тестам IELTS через бот Telegram."""