var bscoords = require('bscoords');
var fs = require('fs');
var onResponse = function(err, coords) {
    if (err == null) {

        // yandex request
        if (typeof coords.cell != 'undefined') {
            console.log('Cell: { lat: ' + coords.cell.lat + ', lon: ' + coords.cell.lon + ' }');
            console.log( 'BTS: { lat: ' + coords.bs.lat   + ', lon: ' + coords.bs.lon   + ' }');

            // everything but not yandex
        } else {
            console.log('Resp: { lat: ' + coords.lat + ', lon: ' + coords.lon + ' }');
        }
    }
    else{
        console.log('No response!');
    }

}
var pathToFile="./text.txt";


mcc = process.argv[2];
mnc = process.argv[3];
lac = process.argv[4];
cid = process.argv[5];

/*mcc = "250";
mnc = "02";
lac = "1002";
cid = "41254";*/
var cidCount;
console.log("mcc="+mcc+" mnc="+mnc+" lac="+lac+" cid="+cid);

function doRequest(cidTmp){
    bscoords.requestGoogle(mcc, mnc, lac, cidTmp, onResponse);
    //bscoords.requestYandex(mcc, mnc, lac, cidTmp, onResponse);	
}
doRequest(cid);


/*function rf2m(path){
    var handle=fs.openSync(pathToFile, 'r');
    var list=[], n=[], sdata='';
    do{
        n=fs.readSync(handle, 10, null, 'utf8');
        sdata+=n[0]; //Дописываем к данным то, что получили после последнего '\n'
        var x=sdata.split("\n"); //Разбиваем данные на строки
        sdata=x[x.length-1]; //Пишем в переменную то, что получили после последнего '\n'
        for(var i=0; i<x.length-1;i++){
            list.push(x[i]);
            //fs.writeFileSync('log.txt', x[i]+"\n", {flag:'a'},'binary');
        }
        if(n[1]==0){ //Если длинна порции равна нулю
            if(x[x.length-1]!='') list.push(x[x.length-1]);
            break;
        }
    }while(true)
    fs.closeSync(handle);
    return list;
}

var list = rf2m();
console.log(list);
for (i=1;i<list.length;i++){

    var mcc = list[i].split(",")[0];
    var mnc = list[i].split(",")[1];
    var lac = list[i].split(",")[2];
    var cid = list[i].split(",")[3];

    console.log(list[i]);
    console.log("mcc: "+mcc);
    console.log("mnc: "+mnc);
    console.log("lac: "+lac);
    console.log("cid: "+cid);

    bscoords.requestGoogle(mcc, mnc, lac, cid, onResponse);
}*/
