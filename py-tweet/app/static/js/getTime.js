getTime();

function getTime(){
  var currentTime = new Date()
  var hour = currentTime.getHours()
  var minute = currentTime.getMinutes()
  var second = currentTime.getSeconds()

  if(minute < 10){
    minute = "0" + minute
  }

  if(second < 10){
    second = "0" + second
  }

  var getCurrentTime = hour + ":" + minute + ":" + second + " ";

  if(hour > 11){
    getCurrentTime += "p.m."
  }else{
    getCurrentTime += "a.m."
  }

  document.getElementById("currentTime").innerHTML = "Time now is " + getCurrentTime;
  setTimeout(getTime,1000)
}