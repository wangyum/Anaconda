var ContinuumView, Markup, Paragraph, ParagraphView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

ContinuumView = require("../../common/continuum_view");

Markup = require("./markup");

ParagraphView = (function(superClass) {
  extend(ParagraphView, superClass);

  function ParagraphView() {
    return ParagraphView.__super__.constructor.apply(this, arguments);
  }

  ParagraphView.prototype.tagName = "p";

  ParagraphView.prototype.initialize = function(options) {
    ParagraphView.__super__.initialize.call(this, options);
    this.render();
    return this.listenTo(this.model, 'change', this.render);
  };

  ParagraphView.prototype.render = function() {
    if (this.mget('height')) {
      this.$el.height(this.mget('height'));
    }
    if (this.mget('width')) {
      this.$el.width(this.mget('width'));
    }
    this.$el.text(this.mget('text'));
    return this;
  };

  return ParagraphView;

})(ContinuumView);

Paragraph = (function(superClass) {
  extend(Paragraph, superClass);

  function Paragraph() {
    return Paragraph.__super__.constructor.apply(this, arguments);
  }

  Paragraph.prototype.type = "Paragraph";

  Paragraph.prototype.default_view = ParagraphView;

  Paragraph.prototype.defaults = function() {
    return _.extend({}, Paragraph.__super__.defaults.call(this), {
      text: ''
    });
  };

  return Paragraph;

})(Markup.Model);

module.exports = {
  Model: Paragraph,
  View: ParagraphView
};
