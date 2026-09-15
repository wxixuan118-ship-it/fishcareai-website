(function(){
  var SP={yellow:[75,4,'yellow tang'],kole:[75,4,'kole tang'],tomini:[75,4,'tomini tang'],scopas:[75,4,'scopas tang'],
    purple:[125,6,'purple tang'],convict:[125,6,'convict tang'],blue:[125,6,'blue tang'],powderblue:[125,6,'powder blue tang'],
    chevron:[125,6,'chevron tang'],sailfin:[150,6,'sailfin tang'],achilles:[180,6,'achilles tang'],naso:[180,6,'naso tang'],
    sohal:[240,8,'sohal tang'],clown:[240,8,'clown tang'],vlamingi:[300,8,'vlamingi tang']};
  var STD=[[75,4],[90,4],[125,6],[150,6],[180,6],[240,8],[300,8],[400,8]];
  var $=function(id){return document.getElementById(id)};
  function run(){
    var s=SP[$('tg-sp').value], n=parseInt($('tg-n').value,10), reef=parseFloat($('tg-reef').value), len=parseInt($('tg-len').value,10);
    var base=s[0], minLen=s[1], name=s[2];
    var gal=base*(1+0.5*(n-1))*reef;
    if(n>=2 && minLen<6) minLen=6;
    if(n>=4) minLen=8;
    var pick=null;
    for(var i=0;i<STD.length;i++){ if(STD[i][0]>=gal && STD[i][1]>=minLen){ pick=STD[i]; break; } }
    if(!pick) pick=[Math.ceil(gal/50)*50,8];
    var html='<strong>'+pick[0]+' gallons, at least '+pick[1]+' ft long</strong> for '+(n>1?n+' tangs (largest: '+name+')':'one '+name);
    var note='Calculated need: '+Math.round(gal)+' gal · species minimum '+base+' gal / '+s[1]+' ft'+(n>1?' · +50% per extra tang':'')+(reef>1?' · +20% reef allowance':'')+'.';
    if(len){
      if(len<pick[1]) note+=' A '+len+' ft tank is too short for this setup regardless of volume — '+pick[1]+' ft is the minimum run.';
      else note+=' Your '+len+' ft tank meets the length requirement; make sure it also holds '+pick[0]+' gallons.';
    }
    if(n>1) note+=' Choose different genera and body shapes and add them on the same day.';
    $('tg-result').innerHTML=html+'<p>'+note+'</p>';
  }
  $('tg-go').addEventListener('click',run); run();
})();
