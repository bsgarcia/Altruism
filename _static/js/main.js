import { cardDesc } from './card-desc.js';

// global variables 
var startTime = Date.now();


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

function toggleSlider(enableOnly = false) {
    let div = document.querySelector('.range');
    let slider = document.querySelector('#slider');
    let rangeslider = document.querySelector('#js-rangeslider-0');
    if (div.classList.contains('disabled')) {
        slider.disabled = false;
        document.querySelector('#js-rangeslider-0').disabled = false;
        div.classList.remove('disabled');
        rangeslider.classList.remove('rangeslider-disabled');
        slider.setAttribute('value', 5);
        $('#slider').val(5).change()
        setTimeout(() => {
            slider.dispatchEvent(new Event('change'));
            rangeslider.dispatchEvent(new Event('change'))
        }, 100);
        return
    }

    if (enableOnly)
        return

    slider.setAttribute('value', 0);
    $('#slider').val(0).change()
    slider.disabled = true;
    rangeslider.disabled = true;
    rangeslider.classList.add('rangeslider-disabled');
    div.classList.add('disabled');
    setTimeout(() => {
        slider.dispatchEvent(new Event('change'));
        rangeslider.dispatchEvent(new Event('change'))
    }, 100);
}

const setUpChatButton = () => {
    let btn = document.querySelector('.otree-chat__btn-send');
    btn.className = 'matter-button-contained btn-validate';
    btn.addEventListener('click', () => {
        if (document.querySelector('#input').value.includes('validate')) {
            document.querySelector('#ok').classList.remove('disabled-chat')
            document.querySelector('#ok').disabled = false;
        }
    })
}

const setUpChatInput = () => {
    let el = document.querySelector('.otree-chat__input').cloneNode();
    let realEl = document.querySelector('.otree-chat__input')
    el.className = ''
    el.placeholder = ' '
    let span = document.createElement('span')
    span.id = 'input-text'
    span.innerText = 'Select a message above'
    let label = document.createElement('label')
    label.className = 'matter-textfield-outlined input-chat'
    label.appendChild(el)
    label.appendChild(span)
    realEl.replaceWith(label)
    el.id = 'input'
    document.querySelector('#input').disabled = true;
    // let chat = document.querySelector('.otree-chat')
    // chat.replaceChild(parent, realEl)

}

const setUpSuggestions = () => {
    // Create the parent element
    const messageBox = document.createElement("div");
    messageBox.classList.add("message-box");

    // Create the suggestion elements
    const suggestionCharity = document.createElement("div");
    suggestionCharity.id = "suggestion-charity";
    suggestionCharity.classList.add("suggestion");
    suggestionCharity.textContent = "I want to give to ?";

    const suggestionAmount = document.createElement("div");
    suggestionAmount.id = "suggestion-amount";
    suggestionAmount.classList.add("suggestion");
    suggestionAmount.textContent = "I want to give X euros";

    const suggestionOk = document.createElement("div");
    suggestionOk.id = "suggestion-ok";
    suggestionOk.classList.add("suggestion");
    suggestionOk.textContent = "Ok!";

    const suggestionNo = document.createElement("div");
    suggestionNo.id = "suggestion-no";
    suggestionNo.classList.add("suggestion");
    suggestionNo.textContent = "No!";

    const suggestionValidate = document.createElement("div");
    suggestionValidate.id = "suggestion-validate";
    suggestionValidate.classList.add("suggestion");
    suggestionValidate.textContent = "I will validate";


    // Append the child elements to the parent element
    messageBox.appendChild(suggestionCharity);
    messageBox.appendChild(suggestionAmount);
    messageBox.appendChild(suggestionOk);
    messageBox.appendChild(suggestionNo);
    messageBox.appendChild(suggestionValidate);
    // messageBox.appendChild(messageInput);
    // messageBox.appendChild(sendButton);

    let chat = document.querySelector('.otree-chat');
    let input = document.querySelector('.input-chat');
    chat.insertBefore(messageBox, input);
}

const updateSuggestions = () => {
    document.querySelectorAll('.card').forEach(x => {
        x.addEventListener('click', (event, el) => {
            event.preventDefault();
            if (x.classList.contains('selected'))
                return
            if (document.querySelector('.otree-chat').classList.contains('disabled-chat')) {
                document.querySelector('.otree-chat').classList.add('fade-in')
                document.querySelector('.otree-chat').classList.remove('disabled-chat')
            }
            console.log('clicked ' + x.id);
            document.querySelectorAll('.card').forEach(i => i.classList.remove('selected'));
            x.classList.add('selected');
            document.querySelector('#suggestion-charity').innerHTML = 'I want to give to ' + x.id;
            document.querySelector('#suggestion-amount').style.display = 'block';
            let enableOnly = x.id == 'none' ? false : true;
            toggleSlider(enableOnly = enableOnly);
        });

    })

    document.querySelectorAll('.suggestion').forEach(function (el) {
        el.addEventListener('click', function (el) {
            console.log('clicked suggestion');
            //console.log(el)
            //document.querySelector('#input').disabled = false;
            document.querySelector('#input').value = el.target.innerText;
            document.querySelector('#input').dispatchEvent(new Event('input', { bubbles: true }));
            document.querySelector('#input-text').innerText = 'Select a message above';
            //document.querySelector('#input').disabled = true;

        });
    });
}


const styleChatMessages = () => {
    let msgList = [];

    setInterval(() => {
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

        // check if msg is from me or other
        // for all messages
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
}

const disableChat = () => {
    document.querySelector('.otree-chat').classList.add('disabled-chat');
}

const enableChat = () => {
    document.querySelector('.otree-chat').classList.remove('disabled-chat');
}

const setUpSlider = () => {
    let min = 0;
    let max = window.max;
    let step = 1;
    //let question = 'What was the average value of this symbol?'
    //let question = 'What was the average value of this symbol?'
    let initValue = Math.floor(Math.random() * (8 - 2 + 1)) + 2;
    // generate html
    let sliderHTML = SliderManager.generateSlider({
        text: '',
        min: min, max: max, step: step, initValue: initValue, currency: '£'
    });
    let elSlider = document.createElement('div');
    elSlider.innerHTML = sliderHTML;

    appendElement('slider-div', elSlider);

    // replace suggestion amount by slider value
    document.getElementById('suggestion-amount').innerText = 'I want to give ' + SliderManager.getValue().toString() + ' pounds';

    // listen on events
    SliderManager.listenOnSlider({}, function (event) {
        let value = event.target.value;
        //choice(value, startTime);
    }, function (event) {
        let el = document.getElementById('suggestion-amount');
        // Replace any digit by value of the slider
        el.innerText = el.innerText.replace(/\d+/g, SliderManager.getValue());
        //console.log(value)
        //choice(value, startTime);
    }, '£');

    // allows to change value using left and right arrows
    SliderManager.listenOnArrowKeys();
}

const setUpDescription = () => {
    document.querySelectorAll('.card').forEach(x => {
        if (x.id == 'none') return

        let btnDesc = document.createElement('span');
        let p = document.createElement('p');
        btnDesc.classList.add('btn-desc');
        p.innerText = 'read more';
        let id = x.id.replace(/ /g, '');
        let text = `
        <img class="img-desc" src="/static/img/${id}.png" alt="${id}">
        <br><br>
        <h3><b>Description</b></h3>
        <p>${cardDesc[id]}</p>`;
        btnDesc.addEventListener('click', () => {
            console.log('clicked desc');
            materialAlert('', text, () => console.log('Display description'));
        })
        btnDesc.appendChild(p);
        x.appendChild(btnDesc);
    })
}

const setUpValidation = () => {
    //add event listener to the validate button
    // it opens a material design modal with the confirmation
    document.querySelector('#ok').addEventListener('click', function (el) {
        let slider = document.querySelector('#slider');
        let selected = document.querySelector('.selected');
        materialConfirm('Confirmation', `You chose to give <b>${slider.value}</b> pound(s) to
            <b>${selected.getAttribute('id')}</b>.<br><br>
            Please note that if the other player selected another answer
            than you (i.e. you did not coordinate with each other) the money will be lost.`,
            // if ok is clicked, submit the form
            submit);
        // document.querySelector('#modal').style.display = 'block';
    });

    // disable the button by default
    document.querySelector('#ok').disabled = true
    document.querySelector('#ok').classList.add('disabled-chat')
}


const setUpChat = () => {
    disableChat()
    setUpChatButton();
    styleChatMessages();
    setUpChatInput()
    setUpSuggestions()
    updateSuggestions()
}

const setUp = async () => {
    //await toggleLoading()
    setUpChat()
    setUpSlider()
    setUpValidation()
    setUpDescription()
    //await toggleLoading()
}

const submit = () => {
    let choice = document.querySelector('.card.selected').id
    let contribution = SliderManager.getValue()
    let rt = Date.now() - startTime
    let [msg_html, msg_clean, msg_json] = getMessages()

    liveSend({
        choice: choice,
        contribution: contribution,
        rt: rt,
        msg_html: msg_html,
        msg_clean: msg_clean,
        msg_json: msg_json
    })

    document.querySelector('form').dispatchEvent(new Event('submit'));
}

const getMessages = () => {
    let html = document.querySelector('.otree-chat__messages').innerHTML
    let msgBox = Array.from(document.querySelector('.otree-chat__messages').children)
    let clean = ''
    let i = 0;
    let json = [];
    msgBox.forEach(x => {
        i += 1
        if (x.classList.contains('otree-chat__msg-other')) {
            clean += `number=${i},sender=other,msg=${x.innerText};`
            json.push({
                number: i,
                sender: 'other',
                msg: x.innerText
            })

        } else {
            clean += `number=${i},sender=me,msg=${x.innerText};`

            json.push({
                number: i,
                sender: 'me',
                msg: x.innerText
            })
        }
    })

    let json_string = JSON.stringify(json)

    return [html, clean, json_string]

}

const ping = () => {
    setInterval(() => {
        liveSend('ping')
    }, 2000)
}
// const toggleLoading = async () => {
//     let el = document.getElementById('page-loading');
//     if (!el.classList.contains('hide')) {
//         document.querySelector('.otree-body').classList.remove('hide')
//         el.classList.add('hide')
//     } else {
//         el.classList.remove('hide')
//         document.querySelector('.otree-body').classList.add('hide')
//     }   
//     delay(1000)
// }


window.main = async () => {
    // changeTitle('Altruism Game')
    await setUp()
    ping()


    function liveRecv(data) {

        if (data === true) {
            clearInterval(loopSend);
            $('#main').fadeOut(140);
            $('#form').submit();
        }
    }
}

const delay = ms => new Promise(res => setTimeout(res, ms));
