const inputType = document.querySelector('#input');
const animation = document.querySelector('#animation');
const option = document.querySelector('#option');

var sliderActiveOld = true;
var isSliderActive = function(){return (animation.value == "flash" || animation.value == "bright-wave")};

var changeOptionValue;
(changeOptionValue = function(){
    var trigger = inputType.value;
    var anim = animation.value;

    var sliderActive = isSliderActive();

    var li = document.querySelector(`#${trigger}_${anim}`);
    if(!li) { return }
    var value = li.dataset.value;
    
    if (sliderActive) {
        option.children[1].value = value;
    } else {
        value = value.split(',').forEach(function(color, index){
            option.children[index + 2].value = color;
        });
    }
})();

var changeInputType;
(handleAnimationChange = function(){
    // check if should show slider or color picker
    var sliderActive = isSliderActive();
    // change label and input type
    option.children[0].textContent = sliderActive ? 'Brightness: ' : 'Colors:' ; 
    // hide and disable unwanted inputs
    if (sliderActive != sliderActiveOld){
        for(var i = 1; i < option.children.length; ++i) {
            option.children[i].toggleAttribute('disabled');
            option.children[i].style.display = sliderActive ? 'none' : 'inline';
        }
        option.children[1].style.display = !sliderActive  ? 'none' : 'inline';
        sliderActiveOld = sliderActive;
    }
    changeOptionValue();
})();
