$(document).ready(function(){
	AOS.init({ disable: 'mobile' });
});
$('.owl-carousel').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    center:true,
    dots:false,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:2
        },
        1200:{
          items:2
        }
    }
})

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
  }
  
  /* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
  }

  function openNote() {
    document.getElementById("myNote").style.width = "100%";
  }
  
  function closeNote() {
    document.getElementById("myNote").style.width = "0";
  }
  function openSearch() {
    document.getElementById("mySearch").style.width = "100%";
  }
  
  function closeSearch() {
    document.getElementById("mySearch").style.width = "0";
  }
  function hide(x,y,z){
    var a = document.getElementById(x);
    var b = document.getElementById(y);
    var c= document.getElementById(z);
    if(a.type === 'password'){
      a.type = "text";
      b.style.display = "block";
      c.style.display = "none";
    }
    else {
      a.type = "password";
      b.style.display = "none";
      c.style.display = "block";
    }
  }
var x = document.getElementById('Message');
window.setTimeout("x.style.display='none';", 9000); 

var preloader = document.getElementById('loading');
function loader(){
    preloader.style.display = 'none';
}

$(document).ready(function(){
  $("#myModal").modal('show');
});

var myInput = document.getElementById("password");
var myInput2 = document.getElementById("con_password");
var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");
var con_pass = document.getElementById('con_pass');

// When the user clicks on the password field, show the message box
myInput.onfocus = function() {
  document.getElementById("message").style.display = "block";
}
myInput2.onfocus = function() {
  document.getElementById("message2").style.display = "block";
}

// When the user clicks outside of the password field, hide the message box
myInput.onblur = function() {
  document.getElementById("message").style.display = "none";
}
myInput2.onblur = function() {
  document.getElementById("message2").style.display = "none";
}

// When the user starts to type something inside the password field
myInput.onkeyup = function() {
  // Validate lowercase letters
  var lowerCaseLetters = /[a-z]/g;
  if(myInput.value.match(lowerCaseLetters)) {  
    letter.classList.remove("invalid");
    letter.classList.add("valid");
  } else {
    letter.classList.remove("valid");
    letter.classList.add("invalid");
  }
  
  // Validate capital letters
  var upperCaseLetters = /[A-Z]/g;
  if(myInput.value.match(upperCaseLetters)) {  
    capital.classList.remove("invalid");
    capital.classList.add("valid");
  } else {
    capital.classList.remove("valid");
    capital.classList.add("invalid");
  }

  // Validate numbers
  var numbers = /[0-9]/g;
  if(myInput.value.match(numbers)) {  
    number.classList.remove("invalid");
    number.classList.add("valid");
  } else {
    number.classList.remove("valid");
    number.classList.add("invalid");
  }
  
  // Validate length
  if(myInput.value.length >= 8) {
    length.classList.remove("invalid");
    length.classList.add("valid");
  } else {
    length.classList.remove("valid");
    length.classList.add("invalid");
  }  
}
myInput2.onkeyup = function() {
  // Validate lowercase letters
  if(myInput.value == myInput2.value){
    con_pass.classList.remove("invalid");
    con_pass.classList.add("valid");
  }
  else{
    con_pass.classList.remove("valid");
    con_pass.classList.add("invalid");
  }
}
