var Annotation, Renderer, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Renderer = require("../renderers/renderer");

Annotation = (function(superClass) {
  extend(Annotation, superClass);

  function Annotation() {
    return Annotation.__super__.constructor.apply(this, arguments);
  }

  Annotation.prototype.type = 'Annotation';

  Annotation.prototype.defaults = function() {
    return _.extend({}, Annotation.__super__.defaults.call(this), {
      level: 'overlay',
      plot: null
    });
  };

  return Annotation;

})(Renderer);

module.exports = {
  Model: Annotation
};
