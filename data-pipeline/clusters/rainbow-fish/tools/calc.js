(function(){
  var SP={praecox:[20,30,8,'dwarf neon rainbowfish'],threadfin:[20,30,8,'threadfin rainbowfish'],forktail:[20,30,8,'forktail blue-eyes'],gertrudae:[15,24,8,"Gertrude's blue-eyes"],
    celebes:[30,30,6,'celebes rainbowfish'],boesemani:[40,36,6,'boesemani rainbowfish'],turquoise:[45,36,6,'turquoise rainbowfish'],neonblue:[40,36,6,'neon-blue rainbowfish'],
    australian:[55,48,6,'Australian rainbowfish'],splendid:[55,48,6,'splendid rainbowfish'],parkinsoni:[55,48,6,"Parkinson's rainbowfish"],red:[75,48,6,'red rainbowfish']};
  var STD=[[15,24],[20,30],[29,30],[40,36],[55,48],[75,48],[90,48],[125,72],[180,72]];
  var $=function(id){return document.getElementById(id)};
  function run(){
    var s=SP[$('rf-sp').value], n=parseInt($('rf-n').value,10), s2=SP[$('rf-sp2').value]||null, plant=parseFloat($('rf-plant').value);
    var base=s[0], minLen=s[1], school=s[2], name=s[3];
    var extra=Math.max(0,n-school);
    var gal=base*(1+0.12*extra);
    var note='School minimum '+base+' gal / '+minLen+' in for '+school+' '+name;
    if(extra) note+=' · +12% × '+extra+' extra fish';
    if(s2){ gal+=s2[0]*0.7; minLen=Math.max(minLen,s2[1]); note+=' · +70% of the '+s2[3]+' minimum ('+s2[0]+' gal), each species in its own school of '+s2[2]+'+'; }
    if(plant>1){ gal*=plant; note+=' · +10% heavily planted'; }
    var pick=null;
    for(var i=0;i<STD.length;i++){ if(STD[i][0]>=gal && STD[i][1]>=minLen){ pick=STD[i]; break; } }
    if(!pick) pick=[Math.ceil(gal/25)*25,72];
    var warn='';
    if(n<school) warn=' Fewer than '+school+' is not a school for this species; the calculator assumes '+school+'.';
    $('rf-result').innerHTML='<strong>'+pick[0]+' gallons, at least '+pick[1]+' inches long</strong> for '+Math.max(n,school)+' '+name+(s2?' plus a school of '+s2[3]:'')+'<p>Calculated need '+Math.round(gal)+' gal. '+note+'.'+warn+'</p>';
  }
  $('rf-go').addEventListener('click',run); run();
})();
