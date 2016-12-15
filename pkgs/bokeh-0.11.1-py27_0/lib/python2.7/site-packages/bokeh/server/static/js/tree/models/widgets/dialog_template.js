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
      __out.push('<div class="bk-bs-modal" tabindex="-1">\n  <div class="bk-bs-modal-dialog">\n    <div class="bk-bs-modal-content">\n      <div class="bk-bs-modal-header">\n        ');
    
      if (this.closable) {
        __out.push('\n          <button type="button" class="bk-bs-close" data-bk-bs-dismiss="modal">&times;</button>\n        ');
      }
    
      __out.push('\n        <h4 class="bk-bs-modal-title">');
    
      __out.push(__sanitize(this.title));
    
      __out.push('</h4>\n      </div>\n      <div class="bk-bs-modal-body">\n        <div class="bk-dialog-content" />\n      </div>\n      <div class="bk-bs-modal-footer">\n        <div class="bk-dialog-buttons_box" />\n      </div>\n    </div>\n  </div>\n</div>\n');
    
    }).call(this);
    
  }).call(__obj);
  __obj.safe = __objSafe, __obj.escape = __escape;
  return __out.join('');
};