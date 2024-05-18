// vue.config.js
module.exports = {
    outputDir: '../backend/static',  // 将生成的静态文件输出到 Flask 应用的静态文件目录中
    assetsDir: 'static',
    indexPath: '../templates/index.html',  // 指定生成的 index.html 文件的位置
    devServer: {
        proxy: 'http://127.0.0.1:5000'  // 代理 API 请求到 Flask 后端
      }
  }
  