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
        const quest = ["У кого-нибудь вел <i><b>#преподаватель</b></i>?", "Может у кого-то <i><b>#преподаватель</b></i> принимал, как он?", "А как вообще <i><b>#преподаватель</b></i> на парах?", "Ребята, у кого принимал <i><b>#преподаватель</b></i>? К чему готовиться?", "Расскажите кто-нибудь как проходит занятие с <i><b>#преподаватель</b></i>? Просто чтобы знать к чему готовиться", "Народ, у кого вела <i><b>#преподаватель</b></i>? Что требует знать?", "Кто-нибудь что-нибудь знает про <i><b>#преподаватель</b></i>?", "У кого <i><b>#преподаватель</b></i> вела?", "Товарищи, расскажите про <i><b>#преподаватель</b></i>.", "Что особо любит <i><b>#преподаватель</b></i>?"  ];
        const answ = ["Могу только сказать про <i><b>#преподаватель</b></i>, мы просто каждое занятие писали.", "<i><b>#преподаватель</b></i> очень добрый и адекватный.", "<i><b>#преподаватель</b></i> к ответам не докапывался, нужна была суть", "Мне говорили, что <i><b>#преподаватель</b></i> очень специфический, нужен свой подход", "<i><b>#преподаватель</b></i> - ужас, все вопросы спрашивал, если запинаешься.", "<i><b>#преподаватель</b></i> лишнего не спрашивал. Обстановка спокойная. Всё по билету.", "Знакомый <i><b>#преподаватель</b></i> отвечал, он без проблем поставил по среднему баллу оценку. Ответ прошёл \"безболезненно\".", "<i><b>#преподаватель</b></i> единственный адекватный за 5 лет. Вам очень повезло, что он у вас будет вести.", "<i><b>#преподаватель</b></i> правда замечательный, радуйтесь.", "Вам обязательно нужно будет это прочитать - <i><b>#преподаватель</b></i> требует.", "Этому удели особое внимание, <i><b>#преподаватель</b></i> особо спрашивает."];
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
        while (i<100) {
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



