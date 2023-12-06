// import { cardDesc } from './card-desc.js';

// global variables 
var startTime = Date.now();

export const cardDesc = {
    savethechildren: `Save the Children believes every child deserves a future. In the United States and around the world,
    we work to give children a healthy start in life, the opportunity to learn and protection from harm.
    We ensure children's unique needs are met and their voices are heard. We deliver lasting results for
    millions of children, including those hardest to reach.`,
    unicef: `Over eight decades, the United Nations Children&#39;s Fund (UNICEF) has built an unprecedented global
    support system for the world's children. UNICEF works to deliver the essentials that give every child
    an equitable chance in life: health care and immunizations, safe water and sanitation, nutrition,
    education, emergency relief and more.`,
    wwf: `World Wildlife Fund (WWF) mission is the conservation of nature. Using the best available scientific
    knowledge and advancing that knowledge where we can, we work to preserve the diversity and
    abundance of life on Earth. We are committed to reversing the degradation of our planet&#39;s natural
    environment and to building a future in which human needs are met in harmony with nature.`,
    thenatureconservancy: `The Nature Conservancy is a leading conservation organization working around the world to protect
    ecologically important lands and waters for nature and people. We address threats to conservation
    involving climate change, fire, fresh water, forests, invasive species, and marine ecosystems. We use
    a science-based approach, and we pursue non-confrontational, pragmatic solutions to conservation
    challenges.`,
    cancerresearchuk: `
    Cancer Research UK is the world’s largest independent cancer research institute. It works on how to
    prevent, diagnose and treat cancer and has benefitted millions of lives over the past 120 years.
    `, 
    alzheimersresearchuk: `
    Alzheimer’s Research UK is the UK’s largest dementia charity, dedicated to funding research to
    understand, diagnose, reduce risk and treat the diseases that cause dementia.
    `
}


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
        slider.setAttribute('value', 3);
        $('#slider').val(3).change()
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


const setUpSlider = () => {
    let min = 0;
    let max = window.max;
    let step = 1;
    //let question = 'What was the average value of this symbol?'
    //let question = 'What was the average value of this symbol?'
    let initValue = Math.floor(Math.random() * 6);
    // generate html
    let sliderHTML = SliderManager.generateSlider({
        text: '',
        min: min, max: max, step: step, initValue: initValue, currency: '£'
    });
    let elSlider = document.createElement('div');
    elSlider.innerHTML = sliderHTML;

    // get slider  div
    // let slider = elSlider.querySelector('#slider-div');
    // append slider div to the page
    // slider.appendChild(elSlider);
    appendElement('slider-div', elSlider);


    // listen on events
    SliderManager.listenOnSlider({}, function (event) {
        let value = event.target.value;
        //choice(value, startTime);
    }, function (event) {
        // Replace any digit by value of the slider
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
        let id = x.id.replace(/ /g, '').replace("'", "")
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

const clickCard = (el) => {
    // if the card is already selected, unselect it
    if (el.classList.contains('selected')) {
        el.classList.remove('selected');
        document.querySelector('#ok').disabled = true
    } else {
        // if another card is selected, unselect it
        if (document.querySelector('.selected')) {
            document.querySelector('.selected').classList.remove('selected');
        }
        // select the clicked card
        el.classList.add('selected');
        document.querySelector('#ok').disabled = false
    }

    // if the card is none, disable the slider
    if (el.id == 'none') {
        toggleSlider()
    }
    
    // if the slider is disabled and the card is not none, enable the slider
    let slider = document.querySelector('#slider');
    if (el.id != 'none' & slider.disabled) {
        toggleSlider()
    }
}

const cardListen = () => {
    document.querySelectorAll('.card').forEach(x => {
        x.addEventListener('click', () => {
            clickCard(x)
        })
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
            `,
            // if ok is clicked, submit the form
            submit);
        // document.querySelector('#modal').style.display = 'block';
    });

    // disable the button by default
    document.querySelector('#ok').disabled = true
}


const setUp = async () => {
    //await toggleLoading()
    setUpSlider()
    setUpValidation()
    setUpDescription()
    cardListen()
    //await toggleLoading()
}

const submit = () => {
    let choice = document.querySelector('.card.selected').id
    let contribution = SliderManager.getValue()
    let rt = Date.now() - startTime

    liveSend({
        choice: choice,
        contribution: contribution,
        rt: rt,
    })

    // for firefox
    document.querySelector('form').dispatchEvent(new Event('submit'));

    // for chrome/edge
    let event = document.createEvent('Event');
    event.initEvent('submit', true, true);
    document.querySelector('form').dispatchEvent(event);
    document.querySelector('form').submit();
}

const ping = () => {
    setInterval(() => {
        liveSend('ping')
    }, 2000)
}

window.notify = async () => {
    if (!window.Notification) {
        console.log('Browser does not support notifications.');
    } else {
        // check if permission is already granted
        if (Notification.permission === 'granted') {
            // show notification here
            var notify = new Notification('Prolific Experiment', {
                body: 'We found a match! The experiment is starting!',
                icon: 'https://pbs.twimg.com/profile_images/1027915667637497861/Ps9JRJOc_400x400.jpg',
            });
        }
    }
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
    //
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

window.test = () => {
    alert('test')
}

const delay = ms => new Promise(res => setTimeout(res, ms));

