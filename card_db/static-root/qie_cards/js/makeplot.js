var FAIL = 2
var PASS = 1
var REM = 0
var DEF = -1

function getStats(data, tests)
{
    var cardDates = []
    for (var i = 0; i < tests.length; i++){
        test = tests[i]
        testDat = data[test]
        for (var card in testDat) {
            if (testDat.hasOwnProperty(card)) {

                var cardDat = testDat[card];

                // Initialize the cardDate element    
                if(!cardDates.hasOwnProperty(card)) {
                    cardDates[card] = [cardDat.date, cardDat.state, cardDat.barcode];
                }

                var curDat = cardDates[card];

                // Update the date if necessary
                if( curDat[0] < cardDat.date){
                    cardDates[card][0] = cardDat.date;
                }

                // Check to see if the state needs to be changed
                if( curDat[1] != FAIL ){
                    if( cardDat.state == FAIL ){
                        cardDates[card][1] = FAIL;
                    } else if( curDat[1] != REM ){
                        if( cardDat.state == DEF || cardDat.state == REM ){
                            cardDates[card][1] = REM;
                        } else if( cardDat.state == PASS ){
                            cardDates[card][1] = PASS;
                        }
                    }
                }
            }
        }
    }
    
    sortable = [];
    for (var card in cardDates){
        if( cardDates[card][0] == -1){
            cardDates[card][0] = data["102"][card].date;
        }
        if( cardDates[card][0] != -1){
            sortable.push([card, cardDates[card]]);
        } else {
            console.log("Card " + card + " did not have a Visual Inspection")
        }
    }
    sortable.sort(function(a, b){return a[1][0] - b[1][0]});
    
    return sortable;
}

function getResults(data, tests)
{
    testDateStat = getStats(data, tests);
   
    passedTotal = 0;
    failedTotal = 0;
    remainingTotal = 0;

    totPass = [];
    totFail = [];
    totRem = [];
    cardsPassed = [];
    cardsFailed = [];
    cardsRem = [];

    for (var i = 0; i < testDateStat.length; i++){
        card = testDateStat[i];
        cardDate = card[1][0];
        cardState = card[1][1];
        cardCode = card[1][2]
        
        switch(cardState) {
            case PASS:
                passedTotal += 1;
                cardsPassed.push(cardCode);
                break;
            case FAIL:
                failedTotal += 1;
                cardsFailed.push(cardCode);
                break;
            case REM:
                remainingTotal += 1;
                cardsRem.push(cardCode);
                break;
        }
        totPass[cardDate] = passedTotal;
        totRem[cardDate] = remainingTotal;
        totFail[cardDate] = failedTotal;
    }

    tAxisPass = [];
    tAxisFail = [];
    tAxisRem = [];
    cAxisPass = [];
    cAxisFail = [];
    cAxisRem = [];
    for ( time in totPass ){
        var d = new Date(0);
        d.setUTCSeconds(time);
        tAxisPass.push(d);
        cAxisPass.push(totPass[time]);
    }
    for ( time in totFail ){
        var d = new Date(0);
        d.setUTCSeconds(time);
        tAxisFail.push(d);
        cAxisFail.push(totFail[time]);
    }
    for ( time in totRem ){
        var d = new Date(0);
        d.setUTCSeconds(time);
        tAxisRem.push(d);
        cAxisRem.push(totRem[time]);
    }
    return [tAxisPass, cAxisPass,
            tAxisFail, cAxisFail, 
            tAxisRem, cAxisRem, 
            cardsPassed, cardsFailed, cardsRem];
}

function getData(tests)
{
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function ()
    {
        makePlot(xhr, tests)
    }
    xhr.open("GET", "../cards/media/cached_data/plots.json", true);
    xhr.send();
}

function makeTable(passed, failed, remaining){
    var pCol = document.getElementById('passedCol');
    var fCol = document.getElementById('failedCol');
    var rCol = document.getElementById('remCol');
    var passedList = document.createElement('ul');
    var failedList = document.createElement('ul');
    var remainingList = document.createElement('ul');

    for(var i = 0; i < passed.length; i++){
        var card = document.createElement('li');
        var link = document.createElement('a');
        link.setAttribute('href', passed[i]);
        link.innerHTML = passed[i];
        card.appendChild(link);
        passedList.appendChild(card);
    }

    for(var i = 0; i < failed.length; i++){
        var card = document.createElement('li');
        var link = document.createElement('a');
        link.setAttribute('href', failed[i]);
        link.innerHTML = failed[i];
        card.appendChild(link);
        failedList.appendChild(card);
    }

    for(var i = 0; i < remaining.length; i++){
        var card = document.createElement('li');
        var link = document.createElement('a');
        link.setAttribute('href', remaining[i]);
        link.innerHTML = remaining[i];
        card.appendChild(link);
        remainingList.appendChild(card);
    }

    passedList.setAttribute('class', 'splitColumns');
    failedList.setAttribute('class', 'splitColumns');
    remainingList.setAttribute('class', 'splitColumns');
    pCol.replaceChild(passedList, pCol.childNodes[0]);
    fCol.replaceChild(failedList, fCol.childNodes[0]);
    rCol.replaceChild(remainingList, rCol.childNodes[0]);
}

function makePlot(xhr, tests)
{
    if (xhr.readyState == 4) {
        var data = JSON.parse(xhr.responseText);
        results = getResults(data, tests);
        makeTable(results[6], results[7], results[8]);

        day = results[0] //day of the month of July
        totPass = results[1]
        totFail = results[3]
        totRem = results[5]
        max_X = Math.max.apply(null,day)+1
        min_X = Math.min.apply(null,day)-1
        max_Y = Math.max.apply(null,totPass)+3
        TESTER = document.getElementById('plot');
        traceFail = {
          x: day,
          y: totFail,
          name: "Failed",
          type: "scatter",
          fill: "tozeroy",
          line: {
            color: "Red"}
        };
        tracePass = {
          x: day,
          y: totPass,
          name: "Passed",
          type: "scatter",
          fill: "tozeroy",
          line: {
            color: "Green"}
        };
        traceRem = {
          x: day,
          y: totRem,
          name: "Incomplete",
          type: "scatter",
          fill: "tozeroy",
          line: {
            color: "Yellow"}
        };
        layout = {
          title: "QIE Cards Passed/Failed/Incomplete",
          marker: {
            colorbar: {
              xpad: 2 //don't think I need this...
            }
          },
          showlegend: true,
          autosize: true,
          xaxis: {
            title:"Days (in July 2016)",
            range: [min_X, max_X]},
          yaxis: {
            title: "Number of Cards",
            range: [0, max_Y]},
          legend: {
            x: 0.2,
            y: 0.5 }};
        Plotly.newPlot(TESTER, [traceFail, tracePass, traceRem], layout);
    }
}
