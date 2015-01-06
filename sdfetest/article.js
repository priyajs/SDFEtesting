// Load necessary Libraries
var system=require('system');

if(system.args[1]){
    //console.log(system.args[1])
    var env=system.args[1];
} else {console.log('must invoke script with "phantomjs <env Name> <PII> <render - 0/1>"')}
if(system.args[2]){
    //console.log(system.args[2])
    var startPII=system.args[2]
} else {console.log('must invoke script with "phantomjs <env Name> <PII> <render - 0/1>"')}

var renderArticles= system.args[3]

if(env=='prod'){
  var url='http://www.sciencedirect.com/science/article/pii/'+startPII;
} else if(env.indexOf('sdfe')>-1){
  var url='http://www.'+env+'.sciencedirect.com/science/article/pii/'+startPII;
} else {
  var url='http://'+env+'-www.sciencedirect.com/science/article/pii/'+startPII;
}
//---------------------------------------------------------------
//	Helper Function waitFor.js -https://github.com/ariya/phantomjs/blob/master/examples/waitfor.js
// 		Referenced: http://www.princeton.edu/~crmarsh/phantomjs/
//---------------------------------------------------------------
/**
 * Wait until the test condition is true or a timeout occurs. Useful for waiting
 * on a server response or for a ui change (fadeIn, etc.) to occur.
 *
 * @param testFx javascript condition that evaluates to a boolean,
 * it can be passed in as a string (e.g.: "1 == 1" or "$('#bar').is(':visible')" or
 * as a callback function.
 * @param onReady what to do when testFx condition is fulfilled,
 * it can be passed in as a string (e.g.: "1 == 1" or "$('#bar').is(':visible')" or
 * as a callback function.
 * @param timeOutMillis the max amount of time to wait. If not specified, 3 sec is used.
 */
//function waitFor(testFx, onReady, timeOutMillis) {
var waitFor = function(testFx, onReady, timeOutMillis) {
    var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 15000, //< Default Max Timout is 15s
        start = new Date().getTime(),
        condition = false,
        interval = setInterval(function() {
            if ( (new Date().getTime() - start < maxtimeOutMillis) && !condition ) {
                // If not time-out yet and condition not yet fulfilled
                condition = (typeof(testFx) === "string" ? eval(testFx) : testFx()); //< defensive code
            } else {
                if(!condition) {
                    // If condition still not fulfilled (timeout but condition is 'false')
                    console.log("'waitFor()' timeout "+env+ ' '+startPII);
                    doRender();
                    phantom.exit(1);
                } else {
                    // Condition fulfilled (timeout and/or condition is 'true')
                    //console.log("'waitFor()' finished in " + (new Date().getTime() - start) + "ms.");
                    typeof(onReady) === "string" ? eval(onReady) : onReady(); //< Do what it's supposed to do once the condition is fulfilled
                    clearInterval(interval); //< Stop this interval
                }
            }
        }, 250); //< repeat check every 500ms
};


//var url='http://www.sciencedirect.com/science/article/pii/S2095254614000271'

//Initialize General Variables
var ttlb=0,resourceWait  = 300,
    maxRenderWait = 10000,
    count=0,
    curReq=0,
    curRes=0,
    renderTimeout,
    forcedRenderTimeout
 ;

// Initialize Page Variable
var page = require('webpage').create();

// Set browser window size
page.viewportSize = {
  width: 1280,
  height: 600
};

page.customHeaders={'Authorization':'Basic '+btoa('sdfe-engineers:Target947Tirpitz')}

page.onResourceReceived = function (res) {
      if(res.id==1 && (!res.stage || res.stage === 'end')){ 
	//console.log('ttlb: '+(res.time.getTime()-startTimer+'ms'));    
	ttlb=res.time.getTime()-startTimer;
      }
  /*if(res.id < 10){
    if (!res.stage || res.stage === 'end') {
        count -= 1;
        console.log(res.id + ' ' + res.status + ' - ' + res.url.split('/')[2] +' - '+res.time.getTime());
    }
  }*/
};


function doRender() {
    //var SDMPii=page.evaluate(function(){return SDM.pm.pii;});
    var SDMPii=startPII;
    tm=Date.now();
    page.render('phantom-'+SDMPii+'-'+tm+ '.png');
     //phantom.exit();
}

//page.onConsoleMessage = function (msg) { console.log(msg); };

//div.refText.svRefs

var startTimer=Date.now();
page.open(url, function(status) {
    //console.log(status);
            if(renderArticles==1){
                doRender()
            }
    if(status==='success'){
    waitFor( //Invoking function to define a wait condition and 
        function(){//Condition upon which to wait
            return page.evaluate(function() {
                //return $("div.refText.svRefs").is(":visible");
                //return $("p.copyright").is(":visible");
	       //If Legacy SD page, look for copyright
	       if(document.querySelector('span.logoScienceDirectImg')){
                return document.querySelector('p.copyright')!==null;
	       }
	       // IF SDFE page, look for copyright 
               else if (document.querySelector('img#sd-logo') || document.querySelector('a#main-logo')){
		return document.querySelector('p#copyright-line')!=null
	       }
            });
        },	
        function(){//What to do when the waitFor condition is met
            var endTimer=Date.now();
            if(endTimer && startTimer){console.log('article:'+(endTimer-startTimer)+'ms ttlb:'+ttlb+'ms');} else {console.log('something failed with timers')}
            if(renderArticles==1){
                doRender()
            }
	    //return (endTimer-startTimer)
            phantom.exit();
        });
    } else {
    	console.log('page not opened successfully')
    	phantom.exit()
    	
    };
});



