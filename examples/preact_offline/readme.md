## 一、JavaScript库格式与浏览器兼容性

### 1. CommonJS格式
- **标识**：常见文件后缀`.js`，内部使用`require()`和`module.exports`
- **设计目标**：用于Node.js服务器环境
- **问题**：在浏览器中会出现`Uncaught ReferenceError: require is not defined`
- **使用场景**：不适合在WebView/浏览器中直接使用

### 2. ES模块格式
- **标识**：后缀`.mjs`或`.module.js`，使用`import`和`export`语法
- **设计目标**：现代浏览器的标准模块系统
- **问题**：加载本地文件时会触发CORS限制，报错`Access has been blocked by CORS policy`
- **使用场景**：使用构建工具或从同源服务器加载时适用

### 3. UMD格式
- **标识**：通常后缀`.umd.js`或`.umd.min.js`
- **设计目标**：Universal Module Definition，兼容各种环境
- **优势**：可在Node.js、AMD和浏览器全局变量中使用
- **使用场景**：需要跨环境通用性时的理想选择

### 4. IIFE格式
- **标识**：常见于压缩版本`.min.js`
- **设计目标**：立即执行函数表达式，直接在浏览器中运行
- **优势**：简单直接，无需模块加载器
- **使用场景**：适合浏览器直接使用，最不容易出错

## 二、Preact库的结构与特性

### 1. 核心组件
- **Preact核心库**：提供虚拟DOM、组件渲染和生命周期功能
- **Hooks库**：提供React风格的Hook API
- **HTM库**：提供无需编译的JSX替代方案

### 2. Preact的特殊性
- **核心库文件**：默认发布的`.min.js`是浏览器可直接使用的IIFE格式
- **Hooks库文件**：默认的`.min.js`是Node.js格式，必须使用`.umd.min.js`在浏览器中使用
- **HTM库**：提供在不使用JSX的情况下编写类似JSX的模板语法能力

### 3. 函数对象结构
- **preact对象**：包含`h`(虚拟DOM创建)和`render`(渲染)等函数
- **preactHooks对象**：包含`useState`、`useEffect`等hook函数
- **htm对象**：提供`bind`方法，通常与`h`函数绑定使用

### 4. 关键API解析
- **h函数**：即hyperscript，JSX背后的底层函数，用于创建虚拟DOM
- **htm.bind(h)**：创建一个模板函数，可以使用类似JSX的模板语法
- **render**：将虚拟DOM渲染到实际DOM中

## 三、WebView环境中的前端库最佳实践

### 1. 库文件选择
- **首选格式**：UMD或IIFE格式的压缩版本
- **正确版本**：对Preact核心使用`.min.js`，对Hooks使用`.umd.min.js`
- **版本锁定**：在URL中明确指定版本号，如`@10.15.1`

### 2. 变量访问方式
- **避免方式**：不使用解构赋值`const { h, render } = preact`
- **推荐方式**：使用直接访问`const myH = preact.h; const myRender = preact.render`
- **原因**：避免变量重复声明问题，特别是当库已在全局作用域定义变量时

### 3. 脚本加载顺序
- **依赖顺序**：先加载核心库，再加载依赖核心库的扩展
- **正确顺序**：preact核心 → hooks库 → htm库

### 4. 离线部署策略
- **下载脚本**：创建专用脚本，指定确切版本和格式
- **版本控制**：使用`.gitignore`排除库文件，但保留下载脚本
- **文件检查**：运行前检查必要的库文件是否存在

### 5. 性能优化
- **使用压缩版本**：`.min.js`体积更小，加载更快
- **避免重复下载**：通过本地存储机制避免每次都下载
- **预加载库**：在实际需要前预先加载库文件

## 四、常见错误与解决方案

### 1. require未定义错误
- **错误**：`Uncaught ReferenceError: require is not defined`
- **原因**：使用了CommonJS格式的库
- **解决**：使用UMD或IIFE格式(`.umd.min.js`或`.min.js`)

### 2. CORS错误
- **错误**：`Access has been blocked by CORS policy`
- **原因**：使用ES模块格式加载本地文件
- **解决**：使用非模块格式或设置本地Web服务器

### 3. 变量重复声明
- **错误**：`Identifier 'h' has already been declared`
- **原因**：解构赋值重新声明了全局变量
- **解决**：使用不同的变量名或直接通过对象属性访问

### 4. HTM绑定问题
- **错误**：无法正确解析JSX风格模板
- **原因**：htm未正确绑定h函数
- **解决**：确保使用`const html = htm.bind(h)`进行绑定

## 五、项目组织最佳实践

### 1. 目录结构
- **分离原则**：Python代码、HTML界面和库文件分离
- **统一位置**：所有库文件放在同一级目录便于管理

### 2. 版本控制
- **包含文件**：Python代码、HTML文件、下载脚本
- **排除文件**：所有第三方库文件(.min.js)

### 3. 部署考虑
- **一键安装**：提供一键下载所有依赖的脚本
- **跨平台**：同时支持Windows和Unix系统
- **错误处理**：提供友好的错误信息和恢复步骤

这份知识总结涵盖了在WebView Python项目中使用Preact进行离线开发的关键知识点，理解这些概念将帮助你避免常见陷阱，并采用最佳实践来组织和维护项目。
