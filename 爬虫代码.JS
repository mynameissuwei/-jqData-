// request 封装的是一个http方法
let request = require('request')
let url = 'http://paiming.funds.hexun.com/cc/zcgtj.aspx?column=fund_num&tag=desc'
// 写入文件的fs
let fs = require('fs')
// 中文转码
let iconv = require('iconv-lite')
// node版的jquery库
let cheerios = require('cheerio')


const options = {
  url,
  encoding : null, //让body 直接是buffer
  // 爬取和讯网的过程,遇见反爬手段,加上header头跳过反爬
  headers: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
  }
};


function callback(error, response, body) {
  // 将请求体解码成gb2312格式
  let buf =  iconv.decode(body, 'gb2312');
  let $ = cheerios.load(buf)
  let titles = $('td.dkred').map(function(index,item){
    return $(this).text()
  })
  titles = Array.from(titles)
  fs.writeFileSync('tag.html',buf)
}


request(options,callback)

