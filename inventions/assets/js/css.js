
// aos
function aos_init() {
  AOS.init({
    duration: 1000,
    easing: 'ease-in-out',
    once: true,
    mirror: false
  });
}
window.addEventListener('load', () => {
  aos_init();
});

// scroll bar
window.onscroll = function() {scrollfunction()};

function scrollfunction() {
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    document.getElementById("progress_bar").style.width = scrolled + "%";
}

window.addEventListener('load', AOS.refresh)

// make sure page is at the start on load
$(document).ready(function(){
    $(this).scrollTop(0);
});              


// show more for dc 3
function showmore_dc3() {
  var dots = document.getElementById("dots");
  var dc3_text = document.getElementById("dc3_text");
  var btnText = document.getElementById("myBtn");
  
  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "Read more";
    dc3_text.style.display = "none";
    
    
  } else {
    dots.style.display = "none";
    btnText.innerHTML = "Read less";
    dc3_text.style.display = "inline";
  }
}

// show more for b737
function showmore_b737() {
  var dots_b737 = document.getElementById("dots_b737");
  var b737_text = document.getElementById("b737_text");
  var btn_b737_Text = document.getElementById("btn");
  
  if (dots_b737.style.display === "none") {
    dots_b737.style.display = "inline";
    btn_b737_Text.innerHTML = "Read more";
    b737_text.style.display = "none";
    
    
  } else {
    dots_b737.style.display = "none";
    btn_b737_Text.innerHTML = "Read less";
    b737_text.style.display = "inline";
  }
}

new PureCounter()