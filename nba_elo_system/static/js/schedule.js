$(document).ready( function () {
    const redColour = "rgb(227, 23, 10)"
    const greenColour = "rgb(41, 191, 18)"

    const RGB_Linear_Shade=(p,c)=>{
        var i=parseInt,r=Math.round,[a,b,c,d]=c.split(","),P=p<0,t=P?0:255*p,P=P?1+p:1-p;
        return"rgb"+(d?"a(":"(")+r(i(a[3]=="a"?a.slice(5):a.slice(4))*P+t)+","+r(i(b)*P+t)+","+r(i(c)*P+t)+(d?","+d:")");
    }

    const Scale_X = p => {
        return 1 * ((p - .4) / (1 - .4))
    }

    document.querySelectorAll("[id^=game]").forEach(element => {
        const gameRows = element.getElementsByTagName('tr')
        const winProbRow = 1 // value is dependant on schedule.html
        const projPointDiffRow = 2 // value is dependant on schedule.html
        var elements = gameRows[winProbRow].getElementsByClassName('left-column')
        const awayWinProbElement = elements[0]
        console.log(awayWinProbElement)
        elements = gameRows[projPointDiffRow].getElementsByClassName('left-column')
        const awayProjPointDiffElement = elements[0]
        elements = gameRows[winProbRow].getElementsByClassName('right-column')
        const homeWinProbElement = elements[0]
        elements = gameRows[projPointDiffRow].getElementsByClassName('right-column')
        const homeProjPointDiffElement = elements[0]
        const awayWinProb = parseFloat(parseInt(awayWinProbElement.textContent)/100)
        const homeWinProb = 1 - awayWinProb
        var awayBackgroundColor = null
        var homeBackgroundColor = null

        if (awayWinProb > 0.5) {
            awayBackgroundColor = RGB_Linear_Shade(1 - Scale_X(awayWinProb), greenColour)
            homeBackgroundColor = RGB_Linear_Shade(1 - Scale_X(awayWinProb), redColour)
        } else if (awayWinProb == 0.5) {
            awayBackgroundColor = RGB_Linear_Shade(1 - Scale_X(awayWinProb), greenColour)
            homeBackgroundColor = awayBackgroundColor
        } else {
            awayBackgroundColor = RGB_Linear_Shade(1 - Scale_X(homeWinProb), redColour)
            homeBackgroundColor = RGB_Linear_Shade(1 - Scale_X(homeWinProb), greenColour)
        }

        awayWinProbElement.style.backgroundColor = awayBackgroundColor
        awayProjPointDiffElement.style.backgroundColor = awayBackgroundColor
        homeWinProbElement.style.backgroundColor = homeBackgroundColor
        homeProjPointDiffElement.style.backgroundColor = homeBackgroundColor
        
    });
} );