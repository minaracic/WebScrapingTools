const puppeteer = require('puppeteer');
const fs = require('fs');
const jm = require('js-meter')
const cpuu = require('cputilization');

// const isPrint = true
// const isKb = true       // or Mb
// const profiler = new jm({isPrint, isKb})

let cnt = 0
let sum = 0
var sampler = cpuu({interval:100});
 
sampler.on('sample', function(sample) {
    //gets executed every 100ms
    let usage = sample.percentageBusy();
    if(!isNaN(usage)){
        sum += usage;
        cnt += 1
    }
    
});

console.log(process.pid)

let total = 0
let start_time = (new Date()).getTime()

let start_urls = []
for(let i = 1; i < 25; i++){
    url = 'https://scrapethissite.com/pages/forms/?page_num=' + i
    start_urls.push(url)
}

try{
    (async () => {
        const browser = await puppeteer.launch({headless:false});
        const page = await browser.newPage();
      
    
        // async function one_scrape(){
            for(let i = 0; i < 24; i++){
                await page.goto(start_urls[i]);
    
                // await page.waitForSelector('tr.team')
                // await page.waitForSelector('td')

                const teams = await page.$$eval('td.name', anchors => {
                    return anchors.map(anchor => anchor.textContent.trim())
                })
                const wins = await page.$$eval('td.wins', anchors => {
                    return anchors.map(anchor => anchor.textContent.trim())
                })

                for(let i = 0; i < teams.length; i++){
                    total+=1
                    fs.appendFile('teams.txt', teams[i] + ', ' + wins[i] + '\n', (err)=>{
                        if(err)throw err
                    })
                }
    
    
            }
            await browser.close().then(()=>{
                sampler.stop();

                let end_time = (new Date()).getTime()
                let total_time = end_time - start_time //[ms]
                console.log(total_time)

                console.log("CPU usage >>> "+ sum/cnt)
            });    
        // }
    
    
    })();
}catch(err){
    console.error(err)
}

