function setActiveCurrentStep(id) {
    $('#instructions').removeClass('active');
    $('#training').removeClass('active');
    $('#experiment').removeClass('active');

    if (!$('#' + id).attr('class').includes('active')) {
        $('#' + id).attr('class', 'md-step active');
    }
}

function changeTitle(title) {
    document.title = title;
}


window.main = () => {
    let msgList = [];
    let previousSender = undefined;

    setInterval(x => {
        let nicknames = Array.from(document.querySelectorAll('.otree-chat__nickname'));

        if (nicknames.length == 0) {
            return;
        }
        // check if first msg is from me or other
        if (nicknames[0].innerText.includes('Me')) {
            nicknames[0].parentNode.classList.add('stamp-me')


        } else {
            nicknames[0].parentNode.classList.add('stamp-other')
        }
        let lastClass = nicknames[0].parentNode.classList[0];

        nicknames.map(el => {

            if (!el.id) {
                el.id = Math.floor(Math.random() * Date.now())
            }

            if (!msgList.includes(el.id)) {
                if (!el.innerText.includes('Me')) {
                    el.parentNode.classList.replace('otree-chat__msg', 'otree-chat__msg-other')
                }
                el.parentNode.style.display = 'block';
                el.parentNode.parentNode.scrollTop = el.parentNode.parentNode.scrollHeight
                msgList.push(el.id);
            }
            if (lastClass != el.parentNode.classList[0]) {
                if (lastClass == 'otree-chat__msg') {
                    el.parentNode.classList.add('stamp-other')
                } else {
                    el.parentNode.classList.add('stamp-me')
                }
                lastClass = el.parentNode.classList[0];
            }

        }
        )

    }, 1000)

    let startTime = Date.now();
    let RT;
    let contribution;

    let min = 0;
    let max = window.max;
    let step = 1;
    //let question = 'What was the average value of this symbol?'
    //let question = 'What was the average value of this symbol?'
    let initValue = Math.floor(Math.random() * (8 - 2 + 1)) + 2;
    // generate html
    let sliderHTML = SliderManager.generateSlider({
        text: '',
        min: min, max: max, step: step, initValue: initValue
    });
    let elSlider = document.createElement('div');
    elSlider.innerHTML = sliderHTML;

    appendElement('slider-div', elSlider);

    // replace suggestion amount by slider value
    //document.getElementById('suggestion-amount').innerText = 'I want to give ' + SliderManager.getValue().toString() + ' euros';

    // listen on events
    SliderManager.listenOnSlider({}, function (event) {
        let value = event.data.slider.value;
        //choice(value, startTime);
    }, function (event) {
        //let el = document.getElementById('suggestion-amount');
        // Replace any digit by value of the slider
        //el.innerText = el.innerText.replace(/\d/g, SliderManager.getValue());
        //console.log(value)
        //choice(value, startTime);
    });

    // allows to change value using left and right arrows
    SliderManager.listenOnArrowKeys();


    function choice(value, startTime) {

        RT = Date.now() - startTime;
        var startTime = Date.now();
        contribution = value;

        //liveSend(
        // RT: RT, 
        //contribution: contribution
        //}
        //contribution: contribution
        //}
        // );

        // setTimeout(() => {
        // $('#main').append(templateWait);
        // $("#modalWait").modal({
        // backdrop: 'static',
        // keyboard: false
        // });
        // $('#modalWait').modal('show');
        // }, 1000);

        // setInterval(() => {
        //     var wait = document.getElementById("wait");

        //     if (wait.innerHTML.length >= 3)
        //         wait.innerHTML = "";
        //     else
        //         wait.innerHTML += ".";

        // }, 1000);

        // loopSend = setInterval(() => {
        //     liveSend(
        //         {
        //             time: Date.now() - startTime,
        //             RT: RT,
        //             contribution: contribution
        //         });
        // }, 1000);
        // }

    }

    function liveRecv(data) {

        if (data === true) {
            clearInterval(loopSend);
            $('#main').fadeOut(140);
            $('#form').submit();
        }
    }
}

