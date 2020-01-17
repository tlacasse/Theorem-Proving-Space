!function(){"use strict";function e(e,t,n,r,o,l){return{tag:e,key:t,attrs:n,children:r,text:o,dom:l,domSize:void 0,state:void 0,events:void 0,instance:void 0}}e.normalize=function(t){return Array.isArray(t)?e("[",void 0,void 0,e.normalizeChildren(t),void 0,void 0):null==t||"boolean"==typeof t?null:"object"==typeof t?t:e("#",void 0,void 0,String(t),void 0,void 0)},e.normalizeChildren=function(t){var n=[];if(t.length){for(var r=null!=t[0]&&null!=t[0].key,o=1;o<t.length;o++)if((null!=t[o]&&null!=t[o].key)!==r)throw new TypeError("Vnodes must either always have keys or never have keys!");for(o=0;o<t.length;o++)n[o]=e.normalize(t[o])}return n};var t=function(){var t,n=arguments[this],r=this+1;if(null==n?n={}:("object"!=typeof n||null!=n.tag||Array.isArray(n))&&(n={},r=this),arguments.length===r+1)t=arguments[r],Array.isArray(t)||(t=[t]);else for(t=[];r<arguments.length;)t.push(arguments[r++]);return e("",n.key,n,t)},n=/(?:(^|#|\.)([^#\.\[\]]+))|(\[(.+?)(?:\s*=\s*("|'|)((?:\\["'\]]|.)*?)\5)?\])/g,r={},o={}.hasOwnProperty;function l(e){for(var t in e)if(o.call(e,t))return!1;return!0}function i(i){if(null==i||"string"!=typeof i&&"function"!=typeof i&&"function"!=typeof i.view)throw Error("The selector must be either a string or a component.");var a=t.apply(1,arguments);return"string"==typeof i&&(a.children=e.normalizeChildren(a.children),"["!==i)?function(t,n){var r=n.attrs,i=e.normalizeChildren(n.children),a=o.call(r,"class"),u=a?r.class:r.className;if(n.tag=t.tag,n.attrs=null,n.children=void 0,!l(t.attrs)&&!l(r)){var s={};for(var c in r)o.call(r,c)&&(s[c]=r[c]);r=s}for(var c in t.attrs)o.call(t.attrs,c)&&"className"!==c&&!o.call(r,c)&&(r[c]=t.attrs[c]);for(var c in null==u&&null==t.attrs.className||(r.className=null!=u?null!=t.attrs.className?String(t.attrs.className)+" "+String(u):u:null!=t.attrs.className?t.attrs.className:null),a&&(r.class=null),r)if(o.call(r,c)&&"key"!==c){n.attrs=r;break}return Array.isArray(i)&&1===i.length&&null!=i[0]&&"#"===i[0].tag?n.text=i[0].children:n.children=i,n}(r[i]||function(e){for(var t,o="div",l=[],i={};t=n.exec(e);){var a=t[1],u=t[2];if(""===a&&""!==u)o=u;else if("#"===a)i.id=u;else if("."===a)l.push(u);else if("["===t[3][0]){var s=t[6];s&&(s=s.replace(/\\(["'])/g,"$1").replace(/\\\\/g,"\\")),"class"===t[4]?l.push(s):i[t[4]]=""===s?s:s||!0}}return l.length>0&&(i.className=l.join(" ")),r[e]={tag:o,attrs:i}}(i),a):(a.tag=i,a)}if(i.trust=function(t){return null==t&&(t=""),e("<",void 0,void 0,t,void 0,void 0)},i.fragment=function(){var n=t.apply(0,arguments);return n.tag="[",n.children=e.normalizeChildren(n.children),n},(a=function(e){if(!(this instanceof a))throw new Error("Promise must be called with `new`");if("function"!=typeof e)throw new TypeError("executor must be a function");var t=this,n=[],r=[],o=s(n,!0),l=s(r,!1),i=t._instance={resolvers:n,rejectors:r},u="function"==typeof setImmediate?setImmediate:setTimeout;function s(e,o){return function a(s){var f;try{if(!o||null==s||"object"!=typeof s&&"function"!=typeof s||"function"!=typeof(f=s.then))u(function(){o||0!==e.length||console.error("Possible unhandled promise rejection:",s);for(var t=0;t<e.length;t++)e[t](s);n.length=0,r.length=0,i.state=o,i.retry=function(){a(s)}});else{if(s===t)throw new TypeError("Promise can't be resolved w/ itself");c(f.bind(s))}}catch(e){l(e)}}}function c(e){var t=0;function n(e){return function(n){t++>0||e(n)}}var r=n(l);try{e(n(o),r)}catch(e){r(e)}}c(e)}).prototype.then=function(e,t){var n,r,o=this._instance;function l(e,t,l,i){t.push(function(t){if("function"!=typeof e)l(t);else try{n(e(t))}catch(e){r&&r(e)}}),"function"==typeof o.retry&&i===o.state&&o.retry()}var i=new a(function(e,t){n=e,r=t});return l(e,o.resolvers,n,!0),l(t,o.rejectors,r,!1),i},a.prototype.catch=function(e){return this.then(null,e)},a.prototype.finally=function(e){return this.then(function(t){return a.resolve(e()).then(function(){return t})},function(t){return a.resolve(e()).then(function(){return a.reject(t)})})},a.resolve=function(e){return e instanceof a?e:new a(function(t){t(e)})},a.reject=function(e){return new a(function(t,n){n(e)})},a.all=function(e){return new a(function(t,n){var r=e.length,o=0,l=[];if(0===e.length)t([]);else for(var i=0;i<e.length;i++)!function(i){function a(e){o++,l[i]=e,o===r&&t(l)}null==e[i]||"object"!=typeof e[i]&&"function"!=typeof e[i]||"function"!=typeof e[i].then?a(e[i]):e[i].then(a,n)}(i)})},a.race=function(e){return new a(function(t,n){for(var r=0;r<e.length;r++)e[r].then(t,n)})},"undefined"!=typeof window){void 0===window.Promise?window.Promise=a:window.Promise.prototype.finally||(window.Promise.prototype.finally=a.prototype.finally);var a=window.Promise}else if("undefined"!=typeof global){void 0===global.Promise?global.Promise=a:global.Promise.prototype.finally||(global.Promise.prototype.finally=a.prototype.finally);a=global.Promise}var u=function(t){var n,r=t&&t.document,o={svg:"http://www.w3.org/2000/svg",math:"http://www.w3.org/1998/Math/MathML"};function l(e){return e.attrs&&e.attrs.xmlns||o[e.tag]}function i(e,t){if(e.state!==t)throw new Error("`vnode.state` must not be modified")}function a(e){var t=e.state;try{return this.apply(t,arguments)}finally{i(e,t)}}function u(){try{return r.activeElement}catch(e){return null}}function s(e,t,n,r,o,l,i){for(var a=n;a<r;a++){var u=t[a];null!=u&&c(e,u,o,i,l)}}function c(t,n,o,i,u){var f=n.tag;if("string"==typeof f)switch(n.state={},null!=n.attrs&&R(n.attrs,n,o),f){case"#":!function(e,t,n){t.dom=r.createTextNode(t.children),w(e,t.dom,n)}(t,n,u);break;case"<":d(t,n,i,u);break;case"[":!function(e,t,n,o,l){var i=r.createDocumentFragment();if(null!=t.children){var a=t.children;s(i,a,0,a.length,n,null,o)}t.dom=i.firstChild,t.domSize=i.childNodes.length,w(e,i,l)}(t,n,o,i,u);break;default:!function(t,n,o,i,a){var u=n.tag,c=n.attrs,f=c&&c.is,d=(i=l(n)||i)?f?r.createElementNS(i,u,{is:f}):r.createElementNS(i,u):f?r.createElement(u,{is:f}):r.createElement(u);if(n.dom=d,null!=c&&function(e,t,n){for(var r in t)j(e,r,null,t[r],n)}(n,c,i),w(t,d,a),!b(n)&&(null!=n.text&&(""!==n.text?d.textContent=n.text:n.children=[e("#",void 0,void 0,n.text,void 0,void 0)]),null!=n.children)){var h=n.children;s(d,h,0,h.length,o,null,i),"select"===n.tag&&null!=c&&function(e,t){if("value"in t)if(null===t.value)-1!==e.dom.selectedIndex&&(e.dom.value=null);else{var n=""+t.value;e.dom.value===n&&-1!==e.dom.selectedIndex||(e.dom.value=n)}"selectedIndex"in t&&j(e,"selectedIndex",null,t.selectedIndex,void 0)}(n,c)}}(t,n,o,i,u)}else!function(t,n,r,o,l){(function(t,n){var r;if("function"==typeof t.tag.view){if(t.state=Object.create(t.tag),null!=(r=t.state.view).$$reentrantLock$$)return;r.$$reentrantLock$$=!0}else{if(t.state=void 0,null!=(r=t.tag).$$reentrantLock$$)return;r.$$reentrantLock$$=!0,t.state=null!=t.tag.prototype&&"function"==typeof t.tag.prototype.view?new t.tag(t):t.tag(t)}if(R(t.state,t,n),null!=t.attrs&&R(t.attrs,t,n),t.instance=e.normalize(a.call(t.state.view,t)),t.instance===t)throw Error("A view cannot return the vnode it received as argument");r.$$reentrantLock$$=null})(n,r),null!=n.instance?(c(t,n.instance,r,o,l),n.dom=n.instance.dom,n.domSize=null!=n.dom?n.instance.domSize:0):n.domSize=0}(t,n,o,i,u)}var f={caption:"table",thead:"table",tbody:"table",tfoot:"table",tr:"tbody",th:"tr",td:"tr",colgroup:"table",col:"colgroup"};function d(e,t,n,o){var l=t.children.match(/^\s*?<(\w+)/im)||[],i=r.createElement(f[l[1]]||"div");"http://www.w3.org/2000/svg"===n?(i.innerHTML='<svg xmlns="http://www.w3.org/2000/svg">'+t.children+"</svg>",i=i.firstChild):i.innerHTML=t.children,t.dom=i.firstChild,t.domSize=i.childNodes.length,t.instance=[];for(var a,u=r.createDocumentFragment();a=i.firstChild;)t.instance.push(a),u.appendChild(a);w(e,u,o)}function h(e,t,n,r,o,l){if(t!==n&&(null!=t||null!=n))if(null==t||0===t.length)s(e,n,0,n.length,r,o,l);else if(null==n||0===n.length)x(e,t,0,t.length);else{var i=null!=t[0]&&null!=t[0].key,a=null!=n[0]&&null!=n[0].key,u=0,f=0;if(!i)for(;f<t.length&&null==t[f];)f++;if(!a)for(;u<n.length&&null==n[u];)u++;if(null===a&&null==i)return;if(i!==a)x(e,t,f,t.length),s(e,n,u,n.length,r,o,l);else if(a){for(var d,h,w,b,E,S=t.length-1,C=n.length-1;S>=f&&C>=u&&(w=t[S],b=n[C],w.key===b.key);)w!==b&&p(e,w,b,r,o,l),null!=b.dom&&(o=b.dom),S--,C--;for(;S>=f&&C>=u&&(d=t[f],h=n[u],d.key===h.key);)f++,u++,d!==h&&p(e,d,h,r,y(t,f,o),l);for(;S>=f&&C>=u&&u!==C&&d.key===b.key&&w.key===h.key;)g(e,w,E=y(t,f,o)),w!==h&&p(e,w,h,r,E,l),++u<=--C&&g(e,d,o),d!==b&&p(e,d,b,r,o,l),null!=b.dom&&(o=b.dom),f++,w=t[--S],b=n[C],d=t[f],h=n[u];for(;S>=f&&C>=u&&w.key===b.key;)w!==b&&p(e,w,b,r,o,l),null!=b.dom&&(o=b.dom),C--,w=t[--S],b=n[C];if(u>C)x(e,t,f,S+1);else if(f>S)s(e,n,u,C+1,r,o,l);else{var j,z,A=o,O=C-u+1,N=new Array(O),T=0,P=0,$=2147483647,I=0;for(P=0;P<O;P++)N[P]=-1;for(P=C;P>=u;P--){null==j&&(j=v(t,f,S+1));var L=j[(b=n[P]).key];null!=L&&($=L<$?L:-1,N[P-u]=L,w=t[L],t[L]=null,w!==b&&p(e,w,b,r,o,l),null!=b.dom&&(o=b.dom),I++)}if(o=A,I!==S-f+1&&x(e,t,f,S+1),0===I)s(e,n,u,C+1,r,o,l);else if(-1===$)for(T=(z=function(e){for(var t=[0],n=0,r=0,o=0,l=m.length=e.length,o=0;o<l;o++)m[o]=e[o];for(var o=0;o<l;++o)if(-1!==e[o]){var i=t[t.length-1];if(e[i]<e[o])m[o]=i,t.push(o);else{for(n=0,r=t.length-1;n<r;){var a=(n>>>1)+(r>>>1)+(n&r&1);e[t[a]]<e[o]?n=a+1:r=a}e[o]<e[t[n]]&&(n>0&&(m[o]=t[n-1]),t[n]=o)}}for(n=t.length,r=t[n-1];n-- >0;)t[n]=r,r=m[r];return m.length=0,t}(N)).length-1,P=C;P>=u;P--)h=n[P],-1===N[P-u]?c(e,h,r,l,o):z[T]===P-u?T--:g(e,h,o),null!=h.dom&&(o=n[P].dom);else for(P=C;P>=u;P--)h=n[P],-1===N[P-u]&&c(e,h,r,l,o),null!=h.dom&&(o=n[P].dom)}}else{var R=t.length<n.length?t.length:n.length;for(u=u<f?u:f;u<R;u++)(d=t[u])===(h=n[u])||null==d&&null==h||(null==d?c(e,h,r,l,y(t,u+1,o)):null==h?k(e,d):p(e,d,h,r,y(t,u+1,o),l));t.length>R&&x(e,t,u,t.length),n.length>R&&s(e,n,u,n.length,r,o,l)}}}function p(t,n,r,o,i,u){var s=n.tag;if(s===r.tag){if(r.state=n.state,r.events=n.events,function(e,t){do{if(null!=e.attrs&&"function"==typeof e.attrs.onbeforeupdate){var n=a.call(e.attrs.onbeforeupdate,e,t);if(void 0!==n&&!n)break}if("string"!=typeof e.tag&&"function"==typeof e.state.onbeforeupdate){var n=a.call(e.state.onbeforeupdate,e,t);if(void 0!==n&&!n)break}return!1}while(0);return e.dom=t.dom,e.domSize=t.domSize,e.instance=t.instance,e.attrs=t.attrs,e.children=t.children,e.text=t.text,!0}(r,n))return;if("string"==typeof s)switch(null!=r.attrs&&_(r.attrs,r,o),s){case"#":!function(e,t){e.children.toString()!==t.children.toString()&&(e.dom.nodeValue=t.children),t.dom=e.dom}(n,r);break;case"<":!function(e,t,n,r,o){t.children!==n.children?(E(e,t),d(e,n,r,o)):(n.dom=t.dom,n.domSize=t.domSize,n.instance=t.instance)}(t,n,r,u,i);break;case"[":!function(e,t,n,r,o,l){h(e,t.children,n.children,r,o,l);var i=0,a=n.children;if(n.dom=null,null!=a){for(var u=0;u<a.length;u++){var s=a[u];null!=s&&null!=s.dom&&(null==n.dom&&(n.dom=s.dom),i+=s.domSize||1)}1!==i&&(n.domSize=i)}}(t,n,r,o,i,u);break;default:!function(t,n,r,o){var i=n.dom=t.dom;o=l(n)||o,"textarea"===n.tag&&(null==n.attrs&&(n.attrs={}),null!=n.text&&(n.attrs.value=n.text,n.text=void 0)),function(e,t,n,r){if(null!=n)for(var o in n)j(e,o,t&&t[o],n[o],r);var l;if(null!=t)for(var o in t)null==(l=t[o])||null!=n&&null!=n[o]||z(e,o,l,r)}(n,t.attrs,n.attrs,o),b(n)||(null!=t.text&&null!=n.text&&""!==n.text?t.text.toString()!==n.text.toString()&&(t.dom.firstChild.nodeValue=n.text):(null!=t.text&&(t.children=[e("#",void 0,void 0,t.text,void 0,t.dom.firstChild)]),null!=n.text&&(n.children=[e("#",void 0,void 0,n.text,void 0,void 0)]),h(i,t.children,n.children,r,null,o)))}(n,r,o,u)}else!function(t,n,r,o,l,i){if(r.instance=e.normalize(a.call(r.state.view,r)),r.instance===r)throw Error("A view cannot return the vnode it received as argument");_(r.state,r,o),null!=r.attrs&&_(r.attrs,r,o),null!=r.instance?(null==n.instance?c(t,r.instance,o,i,l):p(t,n.instance,r.instance,o,l,i),r.dom=r.instance.dom,r.domSize=r.instance.domSize):null!=n.instance?(k(t,n.instance),r.dom=void 0,r.domSize=0):(r.dom=n.dom,r.domSize=n.domSize)}(t,n,r,o,i,u)}else k(t,n),c(t,r,o,u,i)}function v(e,t,n){for(var r=Object.create(null);t<n;t++){var o=e[t];if(null!=o){var l=o.key;null!=l&&(r[l]=t)}}return r}var m=[];function y(e,t,n){for(;t<e.length;t++)if(null!=e[t]&&null!=e[t].dom)return e[t].dom;return n}function g(e,t,n){var o=r.createDocumentFragment();!function e(t,n,r){for(;null!=r.dom&&r.dom.parentNode===t;){if("string"!=typeof r.tag){if(null!=(r=r.instance))continue}else if("<"===r.tag)for(var o=0;o<r.instance.length;o++)n.appendChild(r.instance[o]);else if("["!==r.tag)n.appendChild(r.dom);else if(1===r.children.length){if(null!=(r=r.children[0]))continue}else for(var o=0;o<r.children.length;o++){var l=r.children[o];null!=l&&e(t,n,l)}break}}(e,o,t),w(e,o,n)}function w(e,t,n){null!=n?e.insertBefore(t,n):e.appendChild(t)}function b(e){if(null==e.attrs||null==e.attrs.contenteditable&&null==e.attrs.contentEditable)return!1;var t=e.children;if(null!=t&&1===t.length&&"<"===t[0].tag){var n=t[0].children;e.dom.innerHTML!==n&&(e.dom.innerHTML=n)}else if(null!=e.text||null!=t&&0!==t.length)throw new Error("Child node of a contenteditable must be trusted");return!0}function x(e,t,n,r){for(var o=n;o<r;o++){var l=t[o];null!=l&&k(e,l)}}function k(e,t){var n,r,o,l=0,u=t.state;if("string"!=typeof t.tag&&"function"==typeof t.state.onbeforeremove&&null!=(o=a.call(t.state.onbeforeremove,t))&&"function"==typeof o.then&&(l=1,n=o),t.attrs&&"function"==typeof t.attrs.onbeforeremove&&null!=(o=a.call(t.attrs.onbeforeremove,t))&&"function"==typeof o.then&&(l|=2,r=o),i(t,u),l){if(null!=n){var s=function(){1&l&&((l&=2)||c())};n.then(s,s)}null!=r&&(s=function(){2&l&&((l&=1)||c())},r.then(s,s))}else C(t),S(e,t);function c(){i(t,u),C(t),S(e,t)}}function E(e,t){for(var n=0;n<t.instance.length;n++)e.removeChild(t.instance[n])}function S(e,t){for(;null!=t.dom&&t.dom.parentNode===e;){if("string"!=typeof t.tag){if(null!=(t=t.instance))continue}else if("<"===t.tag)E(e,t);else{if("["!==t.tag&&(e.removeChild(t.dom),!Array.isArray(t.children)))break;if(1===t.children.length){if(null!=(t=t.children[0]))continue}else for(var n=0;n<t.children.length;n++){var r=t.children[n];null!=r&&S(e,r)}}break}}function C(e){if("string"!=typeof e.tag&&"function"==typeof e.state.onremove&&a.call(e.state.onremove,e),e.attrs&&"function"==typeof e.attrs.onremove&&a.call(e.attrs.onremove,e),"string"!=typeof e.tag)null!=e.instance&&C(e.instance);else{var t=e.children;if(Array.isArray(t))for(var n=0;n<t.length;n++){var r=t[n];null!=r&&C(r)}}}function j(e,t,n,o,l){if("key"!==t&&"is"!==t&&null!=o&&!A(t)&&(n!==o||function(e,t){return"value"===t||"checked"===t||"selectedIndex"===t||"selected"===t&&e.dom===u()||"option"===e.tag&&e.dom.parentNode===r.activeElement}(e,t)||"object"==typeof o)){if("o"===t[0]&&"n"===t[1])return L(e,t,o);if("xlink:"===t.slice(0,6))e.dom.setAttributeNS("http://www.w3.org/1999/xlink",t.slice(6),o);else if("style"===t)$(e.dom,n,o);else if(O(e,t,l)){if("value"===t){if(("input"===e.tag||"textarea"===e.tag)&&e.dom.value===""+o&&e.dom===u())return;if("select"===e.tag&&null!==n&&e.dom.value===""+o)return;if("option"===e.tag&&null!==n&&e.dom.value===""+o)return}"input"===e.tag&&"type"===t?e.dom.setAttribute(t,o):e.dom[t]=o}else"boolean"==typeof o?o?e.dom.setAttribute(t,""):e.dom.removeAttribute(t):e.dom.setAttribute("className"===t?"class":t,o)}}function z(e,t,n,r){if("key"!==t&&"is"!==t&&null!=n&&!A(t))if("o"!==t[0]||"n"!==t[1]||A(t))if("style"===t)$(e.dom,n,null);else if(!O(e,t,r)||"className"===t||"value"===t&&("option"===e.tag||"select"===e.tag&&-1===e.dom.selectedIndex&&e.dom===u())||"input"===e.tag&&"type"===t){var o=t.indexOf(":");-1!==o&&(t=t.slice(o+1)),!1!==n&&e.dom.removeAttribute("className"===t?"class":t)}else e.dom[t]=null;else L(e,t,void 0)}function A(e){return"oninit"===e||"oncreate"===e||"onupdate"===e||"onremove"===e||"onbeforeremove"===e||"onbeforeupdate"===e}function O(e,t,n){return void 0===n&&(e.tag.indexOf("-")>-1||null!=e.attrs&&e.attrs.is||"href"!==t&&"list"!==t&&"form"!==t&&"width"!==t&&"height"!==t)&&t in e.dom}var N=/[A-Z]/g;function T(e){return"-"+e.toLowerCase()}function P(e){return"-"===e[0]&&"-"===e[1]?e:"cssFloat"===e?"float":e.replace(N,T)}function $(e,t,n){if(t===n);else if(null==n)e.style.cssText="";else if("object"!=typeof n)e.style.cssText=n;else if(null==t||"object"!=typeof t)for(var r in e.style.cssText="",n)null!=(o=n[r])&&e.style.setProperty(P(r),String(o));else{for(var r in n){var o;null!=(o=n[r])&&(o=String(o))!==String(t[r])&&e.style.setProperty(P(r),o)}for(var r in t)null!=t[r]&&null==n[r]&&e.style.removeProperty(P(r))}}function I(){this._=n}function L(e,t,n){if(null!=e.events){if(e.events[t]===n)return;null==n||"function"!=typeof n&&"object"!=typeof n?(null!=e.events[t]&&e.dom.removeEventListener(t.slice(2),e.events,!1),e.events[t]=void 0):(null==e.events[t]&&e.dom.addEventListener(t.slice(2),e.events,!1),e.events[t]=n)}else null==n||"function"!=typeof n&&"object"!=typeof n||(e.events=new I,e.dom.addEventListener(t.slice(2),e.events,!1),e.events[t]=n)}function R(e,t,n){"function"==typeof e.oninit&&a.call(e.oninit,t),"function"==typeof e.oncreate&&n.push(a.bind(e.oncreate,t))}function _(e,t,n){"function"==typeof e.onupdate&&n.push(a.bind(e.onupdate,t))}return I.prototype=Object.create(null),I.prototype.handleEvent=function(e){var t,n=this["on"+e.type];"function"==typeof n?t=n.call(e.currentTarget,e):"function"==typeof n.handleEvent&&n.handleEvent(e),this._&&!1!==e.redraw&&(0,this._)(),!1===t&&(e.preventDefault(),e.stopPropagation())},function(t,r,o){if(!t)throw new TypeError("Ensure the DOM element being passed to m.route/m.mount/m.render is not undefined.");var l=[],i=u(),a=t.namespaceURI;null==t.vnodes&&(t.textContent=""),r=e.normalizeChildren(Array.isArray(r)?r:[r]);var s=n;try{n="function"==typeof o?o:void 0,h(t,t.vnodes,r,l,null,"http://www.w3.org/1999/xhtml"===a?void 0:a)}finally{n=s}t.vnodes=r,null!=i&&u()!==i&&"function"==typeof i.focus&&i.focus();for(var c=0;c<l.length;c++)l[c]()}}(window),s=function(t,n,r){var o=[],l=!1,i=!1;function a(){if(l)throw new Error("Nested m.redraw.sync() call");l=!0;for(var n=0;n<o.length;n+=2)try{t(o[n],e(o[n+1]),u)}catch(e){r.error(e)}l=!1}function u(){i||(i=!0,n(function(){i=!1,a()}))}return u.sync=a,{mount:function(n,r){if(null!=r&&null==r.view&&"function"!=typeof r)throw new TypeError("m.mount(element, component) expects a component, not a vnode");var l=o.indexOf(n);l>=0&&(o.splice(l,2),t(n,[],u)),null!=r&&(o.push(n,r),t(n,e(r),u))},redraw:u}}(u,requestAnimationFrame,console),c=function(e){if("[object Object]"!==Object.prototype.toString.call(e))return"";var t=[];for(var n in e)r(n,e[n]);return t.join("&");function r(e,n){if(Array.isArray(n))for(var o=0;o<n.length;o++)r(e+"["+o+"]",n[o]);else if("[object Object]"===Object.prototype.toString.call(n))for(var o in n)r(e+"["+o+"]",n[o]);else t.push(encodeURIComponent(e)+(null!=n&&""!==n?"="+encodeURIComponent(n):""))}},f=Object.assign||function(e,t){t&&Object.keys(t).forEach(function(n){e[n]=t[n]})},d=function(e,t){if(/:([^\/\.-]+)(\.{3})?:/.test(e))throw new SyntaxError("Template parameter names *must* be separated");if(null==t)return e;var n=e.indexOf("?"),r=e.indexOf("#"),o=r<0?e.length:r,l=n<0?o:n,i=e.slice(0,l),a={};f(a,t);var u=i.replace(/:([^\/\.-]+)(\.{3})?/g,function(e,n,r){return delete a[n],null==t[n]?e:r?t[n]:encodeURIComponent(String(t[n]))}),s=u.indexOf("?"),d=u.indexOf("#"),h=d<0?u.length:d,p=s<0?h:s,v=u.slice(0,p);n>=0&&(v+=e.slice(n,o)),s>=0&&(v+=(n<0?"?":"&")+u.slice(s,h));var m=c(a);return m&&(v+=(n<0&&s<0?"?":"&")+m),r>=0&&(v+=e.slice(r)),d>=0&&(v+=(r<0?"":"&")+u.slice(d)),v},h=function(e,t,n){var r=0;function o(e){return new t(e)}function l(e){return function(r,l){"string"!=typeof r?(l=r,r=r.url):null==l&&(l={});var i=new t(function(t,n){e(d(r,l.params),l,function(e){if("function"==typeof l.type)if(Array.isArray(e))for(var n=0;n<e.length;n++)e[n]=new l.type(e[n]);else e=new l.type(e);t(e)},n)});if(!0===l.background)return i;var a=0;function u(){0==--a&&"function"==typeof n&&n()}return function e(t){var n=t.then;return t.constructor=o,t.then=function(){a++;var r=n.apply(t,arguments);return r.then(u,function(e){if(u(),0===a)throw e}),e(r)},t}(i)}}function i(e,t){for(var n in e.headers)if({}.hasOwnProperty.call(e.headers,n)&&t.test(n))return!0;return!1}return o.prototype=t.prototype,o.__proto__=t,{request:l(function(t,n,r,o){var l,a=null!=n.method?n.method.toUpperCase():"GET",u=n.body,s=!(null!=n.serialize&&n.serialize!==JSON.serialize||u instanceof e.FormData),c=n.responseType||("function"==typeof n.extract?"":"json"),f=new e.XMLHttpRequest,d=!1,h=f,p=f.abort;for(var v in f.abort=function(){d=!0,p.call(this)},f.open(a,t,!1!==n.async,"string"==typeof n.user?n.user:void 0,"string"==typeof n.password?n.password:void 0),s&&null!=u&&!i(n,/^content0-type1$/i)&&f.setRequestHeader("Content-Type","application/json; charset=utf-8"),"function"==typeof n.deserialize||i(n,/^accept$/i)||f.setRequestHeader("Accept","application/json, text/*"),n.withCredentials&&(f.withCredentials=n.withCredentials),n.timeout&&(f.timeout=n.timeout),f.responseType=c,n.headers)({}).hasOwnProperty.call(n.headers,v)&&f.setRequestHeader(v,n.headers[v]);f.onreadystatechange=function(e){if(!d&&4===e.target.readyState)try{var l,i=e.target.status>=200&&e.target.status<300||304===e.target.status||/^file:\/\//i.test(t),a=e.target.response;if("json"===c?e.target.responseType||"function"==typeof n.extract||(a=JSON.parse(e.target.responseText)):c&&"text"!==c||null==a&&(a=e.target.responseText),"function"==typeof n.extract?(a=n.extract(e.target,n),i=!0):"function"==typeof n.deserialize&&(a=n.deserialize(a)),i)r(a);else{try{l=e.target.responseText}catch(e){l=a}var u=new Error(l);u.code=e.target.status,u.response=a,o(u)}}catch(e){o(e)}},"function"==typeof n.config&&(f=n.config(f,n,t)||f)!==h&&(l=f.abort,f.abort=function(){d=!0,l.call(this)}),null==u?f.send():"function"==typeof n.serialize?f.send(n.serialize(u)):u instanceof e.FormData?f.send(u):f.send(JSON.stringify(u))}),jsonp:l(function(t,n,o,l){var i=n.callbackName||"_mithril_"+Math.round(1e16*Math.random())+"_"+r++,a=e.document.createElement("script");e[i]=function(t){delete e[i],a.parentNode.removeChild(a),o(t)},a.onerror=function(){delete e[i],a.parentNode.removeChild(a),l(new Error("JSONP request failed"))},a.src=t+(t.indexOf("?")<0?"?":"&")+encodeURIComponent(n.callbackKey||"callback")+"="+encodeURIComponent(i),e.document.documentElement.appendChild(a)})}}(window,a,s.redraw),p=s,v=function(){return i.apply(this,arguments)};v.m=i,v.trust=i.trust,v.fragment=i.fragment,v.mount=p.mount;var m=i,y=a,g=function(e){if(""===e||null==e)return{};"?"===e.charAt(0)&&(e=e.slice(1));for(var t=e.split("&"),n={},r={},o=0;o<t.length;o++){var l=t[o].split("="),i=decodeURIComponent(l[0]),a=2===l.length?decodeURIComponent(l[1]):"";"true"===a?a=!0:"false"===a&&(a=!1);var u=i.split(/\]\[?|\[/),s=r;i.indexOf("[")>-1&&u.pop();for(var c=0;c<u.length;c++){var f=u[c],d=u[c+1],h=""==d||!isNaN(parseInt(d,10));if(""===f)null==n[i=u.slice(0,c).join()]&&(n[i]=Array.isArray(s)?s.length:0),f=n[i]++;else if("__proto__"===f)break;if(c===u.length-1)s[f]=a;else{var p=Object.getOwnPropertyDescriptor(s,f);null!=p&&(p=p.value),null==p&&(s[f]=p=h?[]:{}),s=p}}}return r},w=function(e){var t=e.indexOf("?"),n=e.indexOf("#"),r=n<0?e.length:n,o=t<0?r:t,l=e.slice(0,o).replace(/\/{2,}/g,"/");return l?("/"!==l[0]&&(l="/"+l),l.length>1&&"/"===l[l.length-1]&&(l=l.slice(0,-1))):l="/",{path:l,params:t<0?{}:g(e.slice(t+1,r))}},b=function(e){var t=w(e),n=Object.keys(t.params),r=[],o=new RegExp("^"+t.path.replace(/:([^\/.-]+)(\.{3}|\.(?!\.)|-)?|[\\^$*+.()|\[\]{}]/g,function(e,t,n){return null==t?"\\"+e:(r.push({k:t,r:"..."===n}),"..."===n?"(.*)":"."===n?"([^/]+)\\.":"([^/]+)"+(n||""))})+"$");return function(e){for(var l=0;l<n.length;l++)if(t.params[n[l]]!==e.params[n[l]])return!1;if(!r.length)return o.test(e.path);var i=o.exec(e.path);if(null==i)return!1;for(l=0;l<r.length;l++)e.params[r[l].k]=r[l].r?i[l+1]:decodeURIComponent(i[l+1]);return!0}},x={};v.route=function(t,n){var r;function o(e,n,o){if(e=d(e,n),null!=r){r();var l=o?o.state:null,i=o?o.title:null;o&&o.replace?t.history.replaceState(l,i,h.prefix+e):t.history.pushState(l,i,h.prefix+e)}else t.location.href=h.prefix+e}var l,i,a,u,s=x,c=h.SKIP={};function h(d,p,v){if(null==d)throw new Error("Ensure the DOM element that was passed to `m.route` is not undefined");var m,g=0,k=Object.keys(v).map(function(e){if("/"!==e[0])throw new SyntaxError("Routes must start with a `/`");if(/:([^\/\.-]+)(\.{3})?:/.test(e))throw new SyntaxError("Route parameter names must be separated with either `/`, `.`, or `-`");return{route:e,component:v[e],check:b(e)}}),E="function"==typeof setImmediate?setImmediate:setTimeout,S=y.resolve(),C=!1;if(r=null,null!=p){var j=w(p);if(!k.some(function(e){return e.check(j)}))throw new ReferenceError("Default route doesn't match any known routes")}function z(){C=!1;var e=t.location.hash;"#"!==h.prefix[0]&&(e=t.location.search+e,"?"!==h.prefix[0]&&"/"!==(e=t.location.pathname+e)[0]&&(e="/"+e));var r=e.concat().replace(/(?:%[a-f89][a-f0-9])+/gim,decodeURIComponent).slice(h.prefix.length),d=w(r);function v(){if(r===p)throw new Error("Could not resolve default route "+p);o(p,null,{replace:!0})}f(d.params,t.history.state),function e(t){for(;t<k.length;t++)if(k[t].check(d)){var o=k[t].component,f=k[t].route,h=o,p=u=function(f){if(p===u){if(f===c)return e(t+1);l=null==f||"function"!=typeof f.view&&"function"!=typeof f?"div":f,i=d.params,a=r,u=null,s=o.render?o:null,2===g?n.redraw():(g=2,n.redraw.sync())}};return void(o.view||"function"==typeof o?(o={},p(h)):o.onmatch?S.then(function(){return o.onmatch(d.params,r,f)}).then(p,v):p("div"))}v()}(0)}return r=function(){C||(C=!0,E(z))},"function"==typeof t.history.pushState?(m=function(){t.removeEventListener("popstate",r,!1)},t.addEventListener("popstate",r,!1)):"#"===h.prefix[0]&&(r=null,m=function(){t.removeEventListener("hashchange",z,!1)},t.addEventListener("hashchange",z,!1)),n.mount(d,{onbeforeupdate:function(){return!(!(g=g?2:1)||x===s)},oncreate:z,onremove:m,view:function(){if(g&&x!==s){var t=[e(l,i.key,i)];return s&&(t=s.render(t[0])),t}}})}return h.set=function(e,t,n){null!=u&&((n=n||{}).replace=!0),u=null,o(e,t,n)},h.get=function(){return a},h.prefix="#!",h.Link={view:function(e){var t,n,r=e.attrs.options,o={};f(o,e.attrs),o.selector=o.options=o.key=o.oninit=o.oncreate=o.onbeforeupdate=o.onupdate=o.onbeforeremove=o.onremove=null;var l=m(e.attrs.selector||"a",o,e.children);return(l.attrs.disabled=Boolean(l.attrs.disabled))?(l.attrs.href=null,l.attrs["aria-disabled"]="true",l.attrs.onclick=null):(t=l.attrs.onclick,n=l.attrs.href,l.attrs.href=h.prefix+n,l.attrs.onclick=function(e){var o;"function"==typeof t?o=t.call(e.currentTarget,e):null==t||"object"!=typeof t||"function"==typeof t.handleEvent&&t.handleEvent(e),!1===o||e.defaultPrevented||0!==e.button&&0!==e.which&&1!==e.which||e.currentTarget.target&&"_self"!==e.currentTarget.target||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey||(e.preventDefault(),e.redraw=!1,h.set(n,null,r))}),l}},h.param=function(e){return i&&null!=e?i[e]:i},h}(window,p),v.render=u,v.redraw=p.redraw,v.request=h.request,v.jsonp=h.jsonp,v.parseQueryString=g,v.buildQueryString=c,v.parsePathname=w,v.buildPathname=d,v.vnode=e,v.PromisePolyfill=a,"undefined"!=typeof module?module.exports=v:window.m=v}();
function nbsps(n) {
    var result = '';
    for (var i = 0; i < n; i++) {
        result += '\u00A0'
    }
    return result;
}

function nbsp() {
    return nbsps(1);
}

function objectToArray(value) {
    var array = [];
    for (var k in value) {
        if (value.hasOwnProperty(k)) {
            array.push([k, value[k]]);
        }
    }
    return array;
}

var API = {};

API.get = function (url, success) {
    App.wait();
    m.request({
        method: 'GET',
        dataType: 'jsonp',
        url: ('http://localhost:5000/api/' + url),
    }).then(function (data) {
        success(data);
        App.reenable();
    }).catch(function (e) {
        App.showError(e);
        App.reenable();
    });
}

var TO = {};

TO.conjecture = function (data) {
    return {
        id: data[0],
        isTraining: data[1] === 1,
        name: data[2],
        text: data[3],
        tokens: data[4],
    };
}

var Templates = {};

Templates.splitContent = function (left, right) {
    return [
        m('div', { id: 'content-left' }, left),
        m('div', { id: 'content-right' }, right),
    ];
}


﻿var HolstepHelper = {};

HolstepHelper.pad = function (number, n) {
    return ('0'.repeat(n) + String(number)).slice(-n);
}

var Holstep = (function () {
    "use strict";
    var vm = {};

    vm.hasData = false;
    vm.conjecture = {};
    vm.id = null;
    vm.type = null;

    vm._buttonList = null;

    function set_conjecture(type, id) {
        vm.type = type;
        vm.id = id;
        API.get('holstep/conjecture/' + vm.type + '/' + vm.id,
            function (data) {
                vm.conjecture = TO.conjecture(data);
                vm.hasData = true;
            });
    }

    function oninit() {
        vm.hasData = false;
    }

    /////////////////////////////////////////

    function button(name, classes, type, id) {
        return m('a', {
            class: 'navbar-button ' + classes,
            onclick: function () {
                set_conjecture(type, id);
            },
        }, name)
    }

    function buttonList() {
        var list = [];
        for (var i = 1; i <= 9999; i++) {
            list.push(button(HolstepHelper.pad(i, 5) + ' train', 'color-training', 'train', i));
        }
        for (var i = 1; i <= 1411; i++) {
            list.push(button(HolstepHelper.pad(i, 4) + ' test', 'color-testing', 'test', i));
        }
        return list;
    }

    function right() {
        if (vm.id === null) {
            return '';
        }
        return m('pre', JSON.stringify(vm.conjecture, null, 2));
    }

    function view() {
        return Templates.splitContent(
            NavBar.view(),
            [
                m('div', { id: 'holstep-content-left' }, buttonList()),
                m('div', { id: 'holstep-content-right' }, right()),
            ],
        );
    }

    return {
        oninit: oninit,
        view: view,
        set_conjecture: set_conjecture,
        private: function () {
            return vm;
        },
    };
})();

var Info = (function () {
    "use strict";
    var vm = {};

    function content() {
        return [
            m('div', { class: 'section-title' }, 'Info'),
            m('div', { class: 'hrule' }),
            m('br'),
            m('ul', [
                m('li', m('a[href=http://cl-informatik.uibk.ac.at/cek/holstep/]', 'Dataset Link')),
            ]),
            m('br'),
            m('iframe', { src: 'http://cl-informatik.uibk.ac.at/cek/holstep/' })
        ];
    }

    function view() {
        return Templates.splitContent(
            NavBar.view(),
            m('div', { class: 'content-area' }, content()),
        );
    }

    return {
        view: view,
        private: function () {
            return vm;
        },
    };
})();

var NavBar = (function () {
    "use strict";
    var vm = {};

    function it(title, link) {
        return {
            title: title,
            link: link,
        };
    }

    vm.items = [
        it('Info', 'info'),
        it('Holstep', 'holstep'),
    ];

    /////////////////////////////////////////

    function button(item) {
        var classes = 'navbar-button';
        if (m.route.get() === '/' + item.link) {
            classes += ' selected';
        }
        return m(m.route.Link, {
            href: '/' + item.link,
            class: classes,
            oncreate: m.route.link,
        }, item.title)
    }

    function view() {
        return vm.items.map(item => button(item));
    }

    return {
        view: view,
        private: function () {
            return vm;
        },
    };
})();

var root = document.getElementById('page');

m.route(root, '/info', {
    '/info': Info,
    '/holstep': Holstep,
});

var App = {}

App.exception = [['', '']];

App.showError = function (exceptionObject) {
    document.getElementById('message-box').style.display = 'block';
    App.exception = objectToArray(exceptionObject);
}

App.hideError = function () {
    document.getElementById('message-box').style.display = 'none';
}

App.wait = function () {
    document.getElementById('wall').style.display = 'block';
}

App.reenable = function () {
    document.getElementById('wall').style.display = 'none';
}

var MessageBox = (function () {
    "use strict";

    function propertyPairToRow(pair) {
        return (
            m('div', { class: 'message-box-pair' }, [
                m('div', { class: 'message-box-key' }, pair[0]),
                m('div', { class: 'message-box-value' }, pair[1]),
            ])
        );
    }

    function view() {
        return [
            m('div', { class: 'message-box-title' },
                m('button', {
                    class: 'message-box-button',
                    onclick: App.hideError
                }, 'X')
            ),
            m('div', { class: 'message-box-detail' },
                App.exception.map(x => propertyPairToRow(x))
            ),
        ];
    }

    return {
        view: view,
    };
})();

m.mount(document.getElementById('message-box'), MessageBox);

