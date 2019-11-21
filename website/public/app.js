const inputType = document.querySelector('#input');
const animation = document.querySelector('#animation');
const option = document.querySelector('#option');

var sliderActiveOld = true;
var isSliderActive = function(){return (animation.value == "flash" || animation.value == "bright-wave")};

var changeOptionValue;
(changeOptionValue = function(){
    var div = document.querySelector('#' + inputType.value)
    if (div === null) { return }

    var trigger = div.id;
    var animation = div.children[1].className;

    var sliderActive = isSliderActive();

    // add scanning for proper animation
    var value = div.children[1].children[1].dataset.value;

    
    if (sliderActive) {
        option.children[1].value = value;
    } else {
        value = value.split(',').forEach(function(color, index){
            console.log(option.children[index + 2]);
            console.log(color);

            option.children[index + 2].value = color;
        });
        
    }
})();

var handleAnimationChange;
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

// unnecessary?
function removeSetting(li){
    let trigger = li.parentElement.id;
    let animation = li.classname;
    delete drums[trigger][animation];
    console.log(x);
}