var Model, Renderer,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

Model = require("../../model");

Renderer = (function(superClass) {
  extend(Renderer, superClass);

  function Renderer() {
    return Renderer.__super__.constructor.apply(this, arguments);
  }

  Renderer.prototype.type = "Renderer";

  return Renderer;

})(Model);

module.exports = Renderer;
