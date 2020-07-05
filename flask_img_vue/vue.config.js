module.exports = {
    outputDir: '../flask_img/static',   //build输出目录
    assetsDir: 'assets', //静态资源目录（js, css, img）
    lintOnSave: false, //是否开启eslint
    devServer: {
        // open: true, //是否自动弹出浏览器页面
        // host: "localhost",
        // port: '8080',
        // https: false,
        // hotOnly: false,
        proxy: {
            '/recon_pic': {
                target: 'http://localhost:9999',
                changeOrigin: true,
            }
        },
    }
}