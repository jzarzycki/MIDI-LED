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
        let input = document.querySelector('input[type="range"]');
        input.value = value;
    } else {
        let inputs = document.querySelectorAll('input[type="color"]');
        value = value.split(',').forEach(function(color, index){
            inputs[index].value = color;
            handleColorChange.call(inputs[index]);
        });
    }
})();

var changeInputType;
(changeInputType = function(){
    // check if should show slider or color picker
    var sliderActive = isSliderActive();
    // change label and input type
    var label = document.querySelector('label[for="option"]');
    label.textContent = sliderActive ? 'Brightness: ' : 'Colors:' ; 
    // hide and disable unwanted inputs
    var inputs = document.querySelectorAll('#option input');
    if (sliderActive != sliderActiveOld){
        for(var i = 0; i < inputs.length; ++i) {
            inputs[i].toggleAttribute('disabled');
            inputs[i].style.display = sliderActive ? 'none' : 'inline';
        }
        inputs[0].style.display = !sliderActive  ? 'none' : 'inline';
        sliderActiveOld = sliderActive;
    }
    changeOptionValue();
})();


function handleColorChange(){
    this.parentNode.style.backgroundColor = this.value;
}
document.querySelectorAll('input[type="color"]').forEach((x) => {
    x.onchange = handleColorChange;
});
