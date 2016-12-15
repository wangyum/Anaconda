var $, Backbone, HasProps, _, logger,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

$ = require("jquery");

_ = require("underscore");

Backbone = require("backbone");

logger = require("./logging").logger;

HasProps = (function(superClass) {
  extend(HasProps, superClass);

  HasProps.prototype.toString = function() {
    return this.type + "(" + this.id + ")";
  };

  HasProps.prototype.destroy = function(options) {
    HasProps.__super__.destroy.call(this, options);
    return this.stopListening();
  };

  HasProps.prototype.isNew = function() {
    return false;
  };

  HasProps.prototype.attrs_and_props = function() {
    var data, j, len, prop_name, ref;
    data = _.clone(this.attributes);
    ref = _.keys(this.properties);
    for (j = 0, len = ref.length; j < len; j++) {
      prop_name = ref[j];
      data[prop_name] = this.get(prop_name);
    }
    return data;
  };

  function HasProps(attributes, options) {
    this.resolve_ref = bind(this.resolve_ref, this);
    this.convert_to_ref = bind(this.convert_to_ref, this);
    var attrs, defaults;
    this.document = null;
    attrs = attributes || {};
    if (!options) {
      options = {};
    }
    this.cid = _.uniqueId('c');
    this.attributes = {};
    if (options.collection) {
      this.collection = options.collection;
    }
    if (options.parse) {
      attrs = this.parse(attrs, options) || {};
    }
    defaults = _.result(this, 'defaults');
    this.set(defaults, {
      defaults: true
    });
    this._set_after_defaults = {};
    this.set(attrs, options);
    this.changed = {};
    this._base = false;
    this.properties = {};
    this.property_cache = {};
    if (!_.has(attrs, this.idAttribute)) {
      this.id = _.uniqueId(this.type);
      this.attributes[this.idAttribute] = this.id;
    }
    if (!options.defer_initialization) {
      this.initialize.apply(this, arguments);
    }
  }

  HasProps.prototype.forceTrigger = function(changes) {
    var change, changing, j, len, options;
    if (!_.isArray(changes)) {
      changes = [changes];
    }
    options = {};
    changing = this._changing;
    this._changing = true;
    if (changes.length) {
      this._pending = true;
    }
    for (j = 0, len = changes.length; j < len; j++) {
      change = changes[j];
      this.trigger('change:' + change, this, this.attributes[change], options);
    }
    if (changing) {
      return this;
    }
    while (this._pending) {
      this._pending = false;
      this.trigger('change', this, options);
    }
    this._pending = false;
    this._changing = false;
    return this;
  };

  HasProps.prototype.set_obj = function(key, value, options) {
    var attrs, val;
    if (_.isObject(key) || key === null) {
      attrs = key;
      options = value;
    } else {
      attrs = {};
      attrs[key] = value;
    }
    for (key in attrs) {
      if (!hasProp.call(attrs, key)) continue;
      val = attrs[key];
      attrs[key] = this.convert_to_ref(val);
    }
    return this.set(attrs, options);
  };

  HasProps.prototype.set = function(key, value, options) {
    var attrs, j, len, old, resolve_refs, results, toremove, val;
    if (_.isObject(key) || key === null) {
      attrs = key;
      options = value;
    } else {
      attrs = {};
      attrs[key] = value;
    }
    toremove = [];
    for (key in attrs) {
      if (!hasProp.call(attrs, key)) continue;
      val = attrs[key];
      if (!((options != null) && options.defaults)) {
        this._set_after_defaults[key] = true;
      }
      if (_.has(this, 'properties') && _.has(this.properties, key) && this.properties[key]['setter']) {
        this.properties[key]['setter'].call(this, val, key);
        toremove.push(key);
      }
    }
    if (!_.isEmpty(toremove)) {
      attrs = _.clone(attrs);
      for (j = 0, len = toremove.length; j < len; j++) {
        key = toremove[j];
        delete attrs[key];
      }
    }
    if (!_.isEmpty(attrs)) {
      old = {};
      for (key in attrs) {
        value = attrs[key];
        old[key] = this.get(key, resolve_refs = false);
      }
      HasProps.__super__.set.call(this, attrs, options);
      if ((options != null ? options.silent : void 0) == null) {
        results = [];
        for (key in attrs) {
          value = attrs[key];
          results.push(this._tell_document_about_change(key, old[key], this.get(key, resolve_refs = false)));
        }
        return results;
      }
    }
  };

  HasProps.prototype.convert_to_ref = function(value) {
    if (_.isArray(value)) {
      return _.map(value, this.convert_to_ref);
    } else {
      if (value instanceof HasProps) {
        return value.ref();
      }
    }
  };

  HasProps.prototype.add_dependencies = function(prop_name, object, fields) {
    var fld, j, len, prop_spec, results;
    if (!_.isArray(fields)) {
      fields = [fields];
    }
    prop_spec = this.properties[prop_name];
    prop_spec.dependencies = prop_spec.dependencies.concat({
      obj: object,
      fields: fields
    });
    results = [];
    for (j = 0, len = fields.length; j < len; j++) {
      fld = fields[j];
      results.push(this.listenTo(object, "change:" + fld, prop_spec['callbacks']['changedep']));
    }
    return results;
  };

  HasProps.prototype.register_setter = function(prop_name, setter) {
    var prop_spec;
    prop_spec = this.properties[prop_name];
    return prop_spec.setter = setter;
  };

  HasProps.prototype.register_property = function(prop_name, getter, use_cache) {
    var changedep, prop_spec, propchange;
    if (_.isUndefined(use_cache)) {
      use_cache = true;
    }
    if (_.has(this.properties, prop_name)) {
      this.remove_property(prop_name);
    }
    changedep = (function(_this) {
      return function() {
        return _this.trigger('changedep:' + prop_name);
      };
    })(this);
    propchange = (function(_this) {
      return function() {
        var firechange, new_val, old_val;
        firechange = true;
        if (prop_spec['use_cache']) {
          old_val = _this.get_cache(prop_name);
          _this.clear_cache(prop_name);
          new_val = _this.get(prop_name);
          firechange = new_val !== old_val;
        }
        if (firechange) {
          _this.trigger('change:' + prop_name, _this, _this.get(prop_name));
          return _this.trigger('change', _this);
        }
      };
    })(this);
    prop_spec = {
      'getter': getter,
      'dependencies': [],
      'use_cache': use_cache,
      'setter': null,
      'callbacks': {
        changedep: changedep,
        propchange: propchange
      }
    };
    this.properties[prop_name] = prop_spec;
    this.listenTo(this, "changedep:" + prop_name, prop_spec['callbacks']['propchange']);
    return prop_spec;
  };

  HasProps.prototype.remove_property = function(prop_name) {
    var dep, dependencies, fld, j, l, len, len1, obj, prop_spec, ref;
    prop_spec = this.properties[prop_name];
    dependencies = prop_spec.dependencies;
    for (j = 0, len = dependencies.length; j < len; j++) {
      dep = dependencies[j];
      obj = dep.obj;
      ref = dep['fields'];
      for (l = 0, len1 = ref.length; l < len1; l++) {
        fld = ref[l];
        obj.off('change:' + fld, prop_spec['callbacks']['changedep'], this);
      }
    }
    this.off("changedep:" + dep);
    delete this.properties[prop_name];
    if (prop_spec.use_cache) {
      return this.clear_cache(prop_name);
    }
  };

  HasProps.prototype.has_cache = function(prop_name) {
    return _.has(this.property_cache, prop_name);
  };

  HasProps.prototype.add_cache = function(prop_name, val) {
    return this.property_cache[prop_name] = val;
  };

  HasProps.prototype.clear_cache = function(prop_name, val) {
    return delete this.property_cache[prop_name];
  };

  HasProps.prototype.get_cache = function(prop_name) {
    return this.property_cache[prop_name];
  };

  HasProps.prototype.get = function(prop_name, resolve_refs) {
    var ref_or_val;
    if (resolve_refs == null) {
      resolve_refs = true;
    }
    if (_.has(this.properties, prop_name)) {
      return this._get_prop(prop_name);
    } else {
      ref_or_val = HasProps.__super__.get.call(this, prop_name);
      if (!resolve_refs) {
        return ref_or_val;
      }
      return this.resolve_ref(ref_or_val);
    }
  };

  HasProps.prototype._get_prop = function(prop_name) {
    var computed, getter, prop_spec;
    prop_spec = this.properties[prop_name];
    if (prop_spec.use_cache && this.has_cache(prop_name)) {
      return this.property_cache[prop_name];
    } else {
      getter = prop_spec.getter;
      computed = getter.apply(this, [prop_name]);
      if (this.properties[prop_name].use_cache) {
        this.add_cache(prop_name, computed);
      }
      return computed;
    }
  };

  HasProps.prototype.ref = function() {
    var base;
    base = {
      'type': this.type,
      'id': this.id
    };
    if (this._subtype != null) {
      base['subtype'] = this._subtype;
    }
    return base;
  };

  HasProps._is_ref = function(arg) {
    var keys;
    if (_.isObject(arg)) {
      keys = _.keys(arg).sort();
      if (keys.length === 2) {
        return keys[0] === 'id' && keys[1] === 'type';
      }
      if (keys.length === 3) {
        return keys[0] === 'id' && keys[1] === 'subtype' && keys[2] === 'type';
      }
    }
    return false;
  };

  HasProps.prototype.set_subtype = function(subtype) {
    return this._subtype = subtype;
  };

  HasProps.prototype.resolve_ref = function(arg) {
    var model, x;
    if (_.isUndefined(arg)) {
      return arg;
    }
    if (_.isArray(arg)) {
      return (function() {
        var j, len, results;
        results = [];
        for (j = 0, len = arg.length; j < len; j++) {
          x = arg[j];
          results.push(this.resolve_ref(x));
        }
        return results;
      }).call(this);
    }
    if (HasProps._is_ref(arg)) {
      if (arg['type'] === this.type && arg['id'] === this.id) {
        return this;
      } else if (this.document) {
        model = this.document.get_model_by_id(arg['id']);
        if (model === null) {
          throw new Error(this + " refers to " + (JSON.stringify(arg)) + " but it isn't in document " + this._document);
        } else {
          return model;
        }
      } else {
        throw new Error(this + " Cannot resolve ref " + (JSON.stringify(arg)) + " when not in a Document");
      }
    }
    return arg;
  };

  HasProps.prototype.get_base = function() {
    if (!this._base) {
      this._base = require('./base');
    }
    return this._base;
  };

  HasProps.prototype.sync = function(method, model, options) {
    return options.success(model.attributes, null, {});
  };

  HasProps.prototype.defaults = function() {
    return {};
  };

  HasProps.prototype.serializable_in_document = function() {
    return true;
  };

  HasProps.prototype.nonserializable_attribute_names = function() {
    return [];
  };

  HasProps.prototype._get_nonserializable_dict = function() {
    var j, len, n, names, ref;
    if (this.constructor._nonserializable_names_cache == null) {
      names = {};
      ref = this.nonserializable_attribute_names();
      for (j = 0, len = ref.length; j < len; j++) {
        n = ref[j];
        names[n] = true;
      }
      this.constructor._nonserializable_names_cache = names;
    }
    return this.constructor._nonserializable_names_cache;
  };

  HasProps.prototype.attribute_is_serializable = function(attr) {
    return (!(attr in this._get_nonserializable_dict())) && (attr in this.attributes);
  };

  HasProps.prototype.serializable_attributes = function() {
    var attrs, k, nonserializable, ref, v;
    nonserializable = this._get_nonserializable_dict();
    attrs = {};
    ref = this.attributes;
    for (k in ref) {
      v = ref[k];
      if (!(k in nonserializable)) {
        attrs[k] = v;
      }
    }
    return attrs;
  };

  HasProps.prototype.toJSON = function(options) {
    throw new Error("bug: toJSON should not be called on " + this + ", models require special serialization measures");
  };

  HasProps._value_to_json = function(key, value, optional_parent_object) {
    var i, j, len, ref_array, ref_obj, subkey, v;
    if (value instanceof HasProps) {
      return value.ref();
    } else if (_.isArray(value)) {
      ref_array = [];
      for (i = j = 0, len = value.length; j < len; i = ++j) {
        v = value[i];
        if (v instanceof HasProps && !v.serializable_in_document()) {
          console.log("May need to add " + key + " to nonserializable_attribute_names of " + (optional_parent_object != null ? optional_parent_object.constructor.name : void 0) + " because array contains a nonserializable type " + v.constructor.name + " under index " + i);
        } else {
          ref_array.push(HasProps._value_to_json(i, v, value));
        }
      }
      return ref_array;
    } else if (_.isObject(value)) {
      ref_obj = {};
      for (subkey in value) {
        if (!hasProp.call(value, subkey)) continue;
        if (value[subkey] instanceof HasProps && !value[subkey].serializable_in_document()) {
          console.log("May need to add " + key + " to nonserializable_attribute_names of " + (optional_parent_object != null ? optional_parent_object.constructor.name : void 0) + " because value of type " + value.constructor.name + " contains a nonserializable type " + value[subkey].constructor.name + " under " + subkey);
        } else {
          ref_obj[subkey] = HasProps._value_to_json(subkey, value[subkey], value);
        }
      }
      return ref_obj;
    } else {
      return value;
    }
  };

  HasProps.prototype.attributes_as_json = function(include_defaults) {
    var attrs, fail, key, ref, value;
    if (include_defaults == null) {
      include_defaults = true;
    }
    attrs = {};
    fail = false;
    ref = this.serializable_attributes();
    for (key in ref) {
      if (!hasProp.call(ref, key)) continue;
      value = ref[key];
      if (include_defaults) {
        attrs[key] = value;
      } else if (key in this._set_after_defaults) {
        attrs[key] = value;
      }
      if (value instanceof HasProps && !value.serializable_in_document()) {
        console.log("May need to add " + key + " to nonserializable_attribute_names of " + this.constructor.name + " because value " + value.constructor.name + " is not serializable");
        fail = true;
      }
    }
    if (fail) {
      return {};
    }
    return HasProps._value_to_json("attributes", attrs, this);
  };

  HasProps._json_record_references = function(doc, v, result, recurse) {
    var elem, j, k, len, model, results, results1;
    if (v === null) {

    } else if (HasProps._is_ref(v)) {
      if (!(v.id in result)) {
        model = doc.get_model_by_id(v.id);
        return HasProps._value_record_references(model, result, recurse);
      }
    } else if (_.isArray(v)) {
      results = [];
      for (j = 0, len = v.length; j < len; j++) {
        elem = v[j];
        results.push(HasProps._json_record_references(doc, elem, result, recurse));
      }
      return results;
    } else if (_.isObject(v)) {
      results1 = [];
      for (k in v) {
        if (!hasProp.call(v, k)) continue;
        elem = v[k];
        results1.push(HasProps._json_record_references(doc, elem, result, recurse));
      }
      return results1;
    }
  };

  HasProps._value_record_references = function(v, result, recurse) {
    var elem, immediate, j, k, l, len, len1, obj, results, results1, results2;
    if (v === null) {

    } else if (v instanceof HasProps) {
      if (!(v.id in result)) {
        result[v.id] = v;
        if (recurse) {
          immediate = v._immediate_references();
          results = [];
          for (j = 0, len = immediate.length; j < len; j++) {
            obj = immediate[j];
            results.push(HasProps._value_record_references(obj, result, true));
          }
          return results;
        }
      }
    } else if (_.isArray(v)) {
      results1 = [];
      for (l = 0, len1 = v.length; l < len1; l++) {
        elem = v[l];
        if (elem instanceof HasProps && !elem.serializable_in_document()) {
          console.log("Array contains nonserializable item, we shouldn't traverse this property ", elem);
          throw new Error("Trying to record refs for array with nonserializable item");
        }
        results1.push(HasProps._value_record_references(elem, result, recurse));
      }
      return results1;
    } else if (_.isObject(v)) {
      results2 = [];
      for (k in v) {
        if (!hasProp.call(v, k)) continue;
        elem = v[k];
        if (elem instanceof HasProps && !elem.serializable_in_document()) {
          console.log("Dict contains nonserializable item under " + k + ", we shouldn't traverse this property ", elem);
          throw new Error("Trying to record refs for dict with nonserializable item");
        }
        results2.push(HasProps._value_record_references(elem, result, recurse));
      }
      return results2;
    }
  };

  HasProps.prototype._immediate_references = function() {
    var attrs, key, result, value;
    result = {};
    attrs = this.serializable_attributes();
    for (key in attrs) {
      value = attrs[key];
      if (value instanceof HasProps && !value.serializable_in_document()) {
        console.log("May need to add " + key + " to nonserializable_attribute_names of " + this.constructor.name + " because value " + value.constructor.name + " is not serializable");
      }
      HasProps._value_record_references(value, result, false);
    }
    return _.values(result);
  };

  HasProps.prototype.attach_document = function(doc) {
    var c, first_attach, j, len, ref, results;
    if (this.document !== null && this.document !== doc) {
      throw new Error("Models must be owned by only a single document");
    }
    first_attach = this.document === null;
    this.document = doc;
    if (doc !== null) {
      doc._notify_attach(this);
      if (first_attach) {
        ref = this._immediate_references();
        results = [];
        for (j = 0, len = ref.length; j < len; j++) {
          c = ref[j];
          results.push(c.attach_document(doc));
        }
        return results;
      }
    }
  };

  HasProps.prototype.detach_document = function() {
    var c, j, len, ref, results;
    if (this.document !== null) {
      if (this.document._notify_detach(this) === 0) {
        this.document = null;
        ref = this._immediate_references();
        results = [];
        for (j = 0, len = ref.length; j < len; j++) {
          c = ref[j];
          results.push(c.detach_document());
        }
        return results;
      }
    }
  };

  HasProps.prototype._tell_document_about_change = function(attr, old, new_) {
    var new_id, new_ref, new_refs, old_id, old_ref, old_refs;
    if (!this.attribute_is_serializable(attr)) {
      return;
    }
    if (old instanceof HasProps && !old.serializable_in_document()) {
      console.log("May need to add " + attr + " to nonserializable_attribute_names of " + this.constructor.name + " because old value " + old.constructor.name + " is not serializable");
      return;
    }
    if (new_ instanceof HasProps && !new_.serializable_in_document()) {
      console.log("May need to add " + attr + " to nonserializable_attribute_names of " + this.constructor.name + " because new value " + new_.constructor.name + " is not serializable");
      return;
    }
    if (this.document !== null) {
      new_refs = {};
      HasProps._value_record_references(new_, new_refs, false);
      old_refs = {};
      HasProps._value_record_references(old, old_refs, false);
      for (new_id in new_refs) {
        new_ref = new_refs[new_id];
        if (!(new_id in old_refs)) {
          new_ref.attach_document(this.document);
        }
      }
      for (old_id in old_refs) {
        old_ref = old_refs[old_id];
        if (!(old_id in new_refs)) {
          old_ref.detach_document();
        }
      }
      return this.document._notify_change(this, attr, old, new_);
    }
  };

  return HasProps;

})(Backbone.Model);

module.exports = HasProps;
