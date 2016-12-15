var HasProps, Model, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

HasProps = require("./common/has_props");

Model = (function(superClass) {
  extend(Model, superClass);

  function Model() {
    return Model.__super__.constructor.apply(this, arguments);
  }

  Model.prototype.type = "Model";

  Model.prototype.defaults = function() {
    return _.extend({}, Model.__super__.defaults.call(this), {
      tags: [],
      name: null
    });
  };

  return Model;

})(HasProps);

module.exports = Model;
