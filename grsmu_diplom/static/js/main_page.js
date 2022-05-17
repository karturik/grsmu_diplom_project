(function () {
    var Message;
    Message = function (arg) {
        this.text = arg.text, this.message_side = arg.message_side;
        this.draw = function (_this) {
            return function () {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);
        return this;
    };
    $(function () {
        const quest = ["У кого-нибудь вел плоцкий гинекологию?", "У кого шило принимал может?", "А как вообще Шило на парах?", "Ребята, у кого принимал Иоскевич? К чему готовиться?", "А кто-нибудь может внятно объяснить как проходит занятие со станько? Просто чтобы знать к чему готовиться", "Народ, у кого вела Могильницкая акушеры в бсмп, хир костюм нужен был?", "кто-нибудь что-нибудь знает про Волынец М. Ю.?", "У кого Сорокопыт педиатрию вела?"   ];
        const answ = ["Могу только сказать про пары, мы просто каждое занятие писали. Переговориться было возможно, но так себе, скорее подглядеть было легче.", "Мужик очень добрый и адекватный.", "К ответам не докапывался, чтобы прям по алгоритму, нужна была суть", "Ну мне сказали, что он оч специфический такой челик и стоит расстроиться", "Каравай тоже, как кого послушать Челик ему сдавал, сказал, пиздец, все вопросы спрашивал, если запинаешься", "Никто лишнего не спрашивал. Обстановка спокойная. Всё по билету, аналогично.", "знакомый ему отвечал, он без проблем поставил по среднему баллу оценку. Ответ прошёл \"безболезненно\".", "Единственный адекватный препод за 5 лет Если боженька поможет он у вас будет вести"];
        var getMessageText, message_side, sendMessage;
        message_side = 'right';
        getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };
        sendMessage = function (text) {
            var $messages, message;
            if (text.trim() === '') {
                return;
            }
            $('.message_input').val('');
            $messages = $('.messages');
            message_side = message_side === 'left' ? 'right' : 'left';
            message = new Message({
                text: text,
                message_side: message_side
            });
            message.draw();
            return $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
        };
        $('.send_message').click(function (e) {
            return sendMessage(getMessageText());
        });
        $('.message_input').keyup(function (e) {
            if (e.which === 13) {
                return sendMessage(getMessageText());
            }
        });

//        sendMessage(quest[Math.floor(Math.random() * quest.length)]);
        sendMessage("Привет");

        let i = 1;
        let time = 2000;
        while (i<10) {
        setTimeout(function () {
            return sendMessage(quest[Math.floor(Math.random() * quest.length)]);
        }, time); time+=2000
        setTimeout(function () {
            return sendMessage(answ[Math.floor(Math.random() * answ.length)]);
        }, time); i++; time+=2800
        };
//        return setTimeout(function () {
//            return sendMessage("3");
//        }, 3000);
    });
}.call(this));



