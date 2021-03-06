��    %      D  5   l      @  c  A  e   �       2   )  .   \  6   �  2   �  1   �  7   '	  3   _	  h  �	    �  F     2   T     �     �     �     �     �  /     ;   F  (   �  R   �     �          2  0   B  ,   s  $   �  6   �  -   �  D   *  /   o  #   �  4   �  1   �    *  �  6  �   $  -   �  f   �  d   c  n   �  a   7  L   �  0   �  Z     �  r  I   %  �   J'  U   �'  3   $(  %   X(  #   ~(  '   �(  $   �(  \   �(  O   L)  =   �)  �   �)  H   �*  *   �*  $   �*  V   +  T   p+  4   �+  ^   �+  �   Y,  �   �,  m   �-  3   �-  c   /.  K   �.                                           %       $                               !   	                 "      #                
                                                        Admin can use following commands:
    * /social_credit_enable - enables Social Credit System for this chat
    * /social_credit_set_chat_option - set a value for a chat option. Takes 2 params: option_name and option value, separated by spaces. Example: `/social_credit_set_chat_option starting_score 300`

Avaliable chat options:
    * starting_score - starting score for anyone, who enrolls to Social Credit System. Default is {start_score}
    * verbosity - bot verbosity level. Can be 0 - answer only to commands, 1 - allow periodical messages, 2 - allow bot reactions. Default is {verbosity}
    * language - bot messages language. Available languages are {languages}. Default is `{language}`, however this can fallback to `en`

For plugins, following management commands are available:
    * /social_credit_plugins - show list of available plugins.
    * /social_credit_enable_plugin - enables plugin. Takes 1 parameter `plugin_name`.
    * /social_credit_disable_plugin - disables plugin. Takes 1 parameter `plugin_name`.
    * /social_credit_plugin_help - shows help text for plugin. Takes 1 parameter `plugin_name`. Automatically sends leaderboard (`/social_credit_chatinfo` command) every day, at {time} o'clock UTC. Available plugins: 
{plugins} Chat is already registered in Social Credit system Chat is not registered in Social Credit system Chat is sucessfully registered in Social Credit system Current Social Credit penises are:
{profile_infos} Current Social Credit scores are:
{profile_infos} Current Social Credit top raters {top_count} are:
{top} Good! {username} Social Credit Score is now {score} I am a control bot of Social Credit Score system for Telegram group chats.
Social Credit Score is manipulated via replies to rankable messages, using this sticker set: https://t.me/addstickers/PoohSocialCredit.
Before use, Social Credit System must be enabled for your chat by a Chat Admin, using /social_credit_enable command.
Then, chat members can enroll to Social Credit System using /social_credit_enroll command.
After enrolling, each member has a {start_score} Starting Credit Score (This can be changed by an admin).
/social_credit_myscore shows your current Social Credit score, while /social_credit_chatinfo command show score info on everyone enrolled into system in this chat.
/social_credit_get_top_raters shows top 10 raters in your chat.
Admins can get help on admin commands using /social_credit_admin_help.
/social_credit_help displays this message again. Implements daily transaction limit: any profile can rank only limited number of messages a day.
Default limit is {limit}, resets every day at {time} o'clock UTC.
Available options:
* limit - changes transaction limit for everyone in the chat. Applies, when limit is reset. Invalid command parameters. Use /social_credit_admin_help for details. Invalid value for option {option}: {error_message} Option {option} set to {value} Plugin is already disabled. Plugin is already enabled. Plugin {plugin} is disabled. Plugin {plugin} is enabled. Profile is not enrolled in Social Credit system Public shame! {username} Social Credit Score is now {score} Ranking your own messages is not allowed Shows chat leaderboard, but in penises. Use /social_credit_chat_penises to see it. Transaction limit exceeded. Unknown option {option} Unknown plugin. You are already enrolled in Social Credit system You are not enrolled in Social Credit system You have already ranked this message You have successfully enrolled in Social Credit system You need to be a Chat Admin to get Admin help You need to be a Chat Admin to register chat in Social Credit system You need to be a Chat Admin to set chat options Your Social Credit score is {score} Your profile is not enrolled in Social Credit system {plugin} plugin option {option} is set to {value} Project-Id-Version: 1.0
POT-Creation-Date: 2020-07-30 19:06+0700
PO-Revision-Date: 2020-08-03 19:06+0700
Last-Translator: ALEKSANDR KAURDAKOV <kapralnsk@gmail.com>
Language: RU
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
 Администратор может использовать следующие команды:
    * /social_credit_enable - регистрирует чат в Системе Социального Рейтинга
    * /social_credit_set_chat_option - выставляет значение для параметра чата. Принимает 2 параметра: option_name и option value, разделенныйх пробелами. Пример: `/social_credit_set_chat_option starting_score 300`
Доступные параметры чата:
    * starting_score - стартовый рейтинг при включении в Систему Социального Рейтинга. Значение по умолчанию: {start_score}
    * verbosity - уровень интерактивности бота (на какие события отправлется сообщения). Может быть 0 - отвечает только на команды, 1 - отправляет периодические сообщения, 2 - разрешает реакции на события в чате. Значение по умолчанию: {verbosity}
    * language - Язык сообщений бота. Доступные языки: {languages}. Язык по умолчанию: `{language}`, однако резервным языком является `en`
Для плагинов доступны следующие команды управления:
        * /social_credit_plugins - показывает список доступных плагинов.
        * /social_credit_enable_plugin - включает плагин. Принимает 1 параметр - имя плагина.
        * /social_credit_disable_plugin - отключает плагин. Принимает 1 параметр - имя плагина.
        * /social_credit_plugin_help - показывает справку по плагину. Принимает 1 параметр - имя плагина.`. Автоматически отправляет рейтинги чата (команду `/social_credit_chatinfo`) каждый день в {time} часов по UTC. Доступные плагины: 
{plugins} Чат уже зарегистрирован в Системе Социального Рейтинга Чат не зарегистрирован в Системе Социального Рейтинга Чат успешно зарегистрирован в Системе Социального Рейтинга Текущие пиписьки Социального Рейтинга чата:
{profile_infos} Текущий Социальный Рейтинг чата:
{profile_infos} Топ {top_count} оценивающих:
{top} Так держать! Социальный Рейтинг {username} теперь {score} Я - контролирующий бот Системы Социального Рейтинга для групповых чатов Telegram.
Социальный Рейтинг может меняться через ответы стикером к сообщениям, из набора https://t.me/addstickers/PoohSocialCredit.
Для использования Системы Социального Рейтинга, она должна быть включена для вашего чата Администратором с помощью команды /social_credit_enable.
Затем, участники чата могут включиться в Систему Социального Рейтинга с помощью команды /social_credit_enroll.
При включении в Систему Социального рейтинга, каждому участнику начисляется {start_score} Социального Рейтинга.
Команда /social_credit_myscore показывает ваш текущий Социальный Рейтинг, а команда /social_credit_chatinfo показывает Социальный Рейтинг всех участников чата, включенных в Систему Социального Рейтинга.
/social_credit_get_top_raters показывает топ 10 оценивающих в вашем чате.
Администраторы могу посмотреть справку по командам администрирования с помощью команды /social_credit_admin_help.
/social_credit_help снова покажет это сообщение. Реализует дневные ограничения на оценки: каждый пользователь может оценить только ограниченное количество сообщений за день.
Ограничение по умолчанию: {limit}, сбрасывается каждый день в {time} по UTC.
Доступные опции:
* limit - меняет количество оценок в день для всех пользователей чата. Применяется во время ежедневного сброса. Недопустимые параметры команды. Используйте /social_credit_admin_help для справки. Недопустимое значение для опции {option}: {error_message} Опция {option} выставлена в {value} Плагин уже отключен. Плагин уже включен. Плагин {plugin} отключен. Плагин {plugin} включен Профиль не включен в Систему Социального Рейтинга Позор! Социальный Рейтинг {username} теперь {score} Оценка своих сообщений запрещена Рейтинги чата, но в пиписьках. Используйте команду /social_credit_chat_penises чтобы на них посмотреть. Превышено количество возможных оценок. Неизвестная опция {option} Неизвестный плагин. Вы уже включены в Систему Социального Рейтинга Вы не включены в Систему Социального Рейтинга Вы уже оценили это сообщение Вы успешно включены в Систему Социального Рейтинга Для справки по командам администрирования нужно быть Администратором чата. Для регистрации чата в Системе Социального Рейтинга, необходимо быть администратором чата Для выставления опций чата нужно быть Администратором чата Ваш Социальный Рейтинг: {score} Ваш профиль не включен в Систему Социального Рейтинга Опция {option} плагина {plugin} выставлена в {value} 