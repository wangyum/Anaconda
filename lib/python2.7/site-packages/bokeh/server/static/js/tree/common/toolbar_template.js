module.exports = function(__obj) {
  if (!__obj) __obj = {};
  var __out = [], __capture = function(callback) {
    var out = __out, result;
    __out = [];
    callback.call(this);
    result = __out.join('');
    __out = out;
    return __safe(result);
  }, __sanitize = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else if (typeof value !== 'undefined' && value != null) {
      return __escape(value);
    } else {
      return '';
    }
  }, __safe, __objSafe = __obj.safe, __escape = __obj.escape;
  __safe = __obj.safe = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else {
      if (!(typeof value !== 'undefined' && value != null)) value = '';
      var result = new String(value);
      result.ecoSafe = true;
      return result;
    }
  };
  if (!__escape) {
    __escape = __obj.escape = function(value) {
      return ('' + value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    };
  }
  (function() {
    (function() {
      if ((this.logo != null) && this.logo === "grey") {
        __out.push('\n  <a href=\'http://bokeh.pydata.org/\' target=\'_blank\' class=\'bk-logo bk-logo-small grey\'></a>\n');
      } else if (this.logo != null) {
        __out.push('\n<a href=\'http://bokeh.pydata.org/\' target=\'_blank\' class=\'bk-logo bk-logo-small\'></a>\n');
      }
    
      __out.push('\n<div class=\'bk-button-bar\'>\n  <ul class=\'bk-button-bar-list\' type="pan" />\n  <ul class=\'bk-button-bar-list\' type="scroll" />\n  <ul class=\'bk-button-bar-list\' type="pinch" />\n  <ul class=\'bk-button-bar-list\' type="tap" />\n  <ul class=\'bk-button-bar-list\' type="press" />\n  <ul class=\'bk-button-bar-list\' type="rotate" />\n  <ul class=\'bk-button-bar-list\' type="actions" />\n  <div class=\'bk-button-bar-list bk-bs-dropdown\' type="inspectors" />\n  <ul class=\'bk-button-bar-list\' type="help" />\n</div>\n');
    
    }).call(this);
    
  }).call(__obj);
  __obj.safe = __objSafe, __obj.escape = __escape;
  return __out.join('');
};