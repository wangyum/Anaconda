var Model, OpenURL, Util, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Util = require("../../util/util");

Model = require("../../model");

OpenURL = (function(superClass) {
  extend(OpenURL, superClass);

  function OpenURL() {
    return OpenURL.__super__.constructor.apply(this, arguments);
  }

  OpenURL.prototype.type = 'OpenURL';

  OpenURL.prototype.execute = function(data_source) {
    var i, j, len, ref, url;
    ref = Util.get_indices(data_source);
    for (j = 0, len = ref.length; j < len; j++) {
      i = ref[j];
      url = Util.replace_placeholders(this.get("url"), data_source, i);
      window.open(url);
    }
    return null;
  };

  OpenURL.prototype.defaults = function() {
    return _.extend({}, OpenURL.__super__.defaults.call(this), {
      url: 'http://'
    });
  };

  return OpenURL;

})(Model);

module.exports = {
  Model: OpenURL
};
