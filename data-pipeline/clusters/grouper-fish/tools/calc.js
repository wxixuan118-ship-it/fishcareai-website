(function(){
  var SP={blueline:[75,48,18,'blue-line hind'],vtail:[75,48,18,'V-tail grouper'],bshind:[100,48,18,'bluespotted hind'],leopard:[100,60,18,'leopard hind'],
    miniatus:[125,60,18,'miniatus grouper'],harlequin:[125,72,18,'harlequin grouper'],panther:[180,72,24,'panther grouper'],argus:[180,72,24,'bluespotted grouper'],
    lyretail:[300,96,30,'lyretail grouper'],red:[300,96,30,'red grouper'],giant:[0,0,0,'bumblebee / giant grouper']};
  var STD=[[75,48,18],[90,48,18],[125,72,18],[150,72,18],[180,72,24],[240,96,24],[300,96,30],[400,96,36],[500,120,36]];
  var $=function(id){return document.getElementById(id)};
  function run(){
    var s=SP[$('gr-sp').value], n=parseInt($('gr-n').value,10), rock=parseFloat($('gr-rock').value), two=$('gr-two').value==='1';
    if(!s[0]){ $('gr-result').innerHTML='<strong>Not a home aquarium fish</strong><p>Bumblebee, giant, goliath and Nassau groupers reach 3–8 feet. Public aquariums only; choose a hind, coral grouper or panther grouper instead.</p>'; return; }
    var base=s[0], minLen=s[1], minW=s[2], name=s[3];
    var gal=base*(1+0.25*n)*rock;
    var note='Base '+base+' gal / '+(minLen/12)+' ft for one adult '+name;
    if(n) note+=' · +25% × '+n+' large tank mate'+(n>1?'s':'');
    if(rock>1) note+=' · +15% rockwork';
    if(two){ gal=Math.max(gal*1.5,300); minLen=Math.max(minLen,96); minW=Math.max(minW,24); note+=' · two groupers: 300-gallon floor, different genera, added together'; }
    var pick=null;
    for(var i=0;i<STD.length;i++){ if(STD[i][0]>=gal && STD[i][1]>=minLen && STD[i][2]>=minW){ pick=STD[i]; break; } }
    if(!pick) pick=[Math.ceil(gal/100)*100,120,36];
    $('gr-result').innerHTML='<strong>'+pick[0]+' gallons, at least '+(pick[1]/12)+' ft long and '+pick[2]+' in wide</strong> for an adult '+name+(n?' with '+n+' large tank mate'+(n>1?'s':''):'')+(two?' and a second grouper':'')+'<p>Calculated need '+Math.round(gal)+' gal. '+note+'. Sized for the adult: the juvenile reaches most of this length within two years.</p>';
  }
  $('gr-go').addEventListener('click',run); run();
})();
