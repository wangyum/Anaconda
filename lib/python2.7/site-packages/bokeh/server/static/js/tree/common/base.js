var Collection, Collections, Config, _, _get_mod_cache, _mod_cache, collection_overrides, index, locations, logger, make_cache, make_collection, url, window,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Collection = require("./collection");

if (typeof window === "undefined" || window === null) {
  window = {
    location: {
      href: "local"
    }
  };
}

logger = require("./logging").logger;

require("./custom").monkey_patch();

Config = {};

url = window.location.href;

if (url.indexOf('/bokeh') > 0) {
  Config.prefix = url.slice(0, url.lastIndexOf('/bokeh')) + "/";
} else {
  Config.prefix = '/';
}

console.log('Bokeh: setting prefix to', Config.prefix);

locations = require("./models");

collection_overrides = {};

make_collection = function(model) {
  var C;
  C = (function(superClass) {
    extend(C, superClass);

    function C() {
      return C.__super__.constructor.apply(this, arguments);
    }

    C.prototype.model = model;

    return C;

  })(Collection);
  return new C();
};

make_cache = function(locations) {
  var mod, modname, name, ref, result, spec, subname, subspec, suffix;
  result = {};
  for (name in locations) {
    spec = locations[name];
    if (_.isArray(spec)) {
      subspec = spec[0];
      suffix = (ref = spec[1]) != null ? ref : "";
      for (subname in subspec) {
        mod = subspec[subname];
        modname = subname + suffix;
        result[modname] = mod;
      }
    } else {
      result[name] = spec;
    }
  }
  return result;
};

_mod_cache = null;

_get_mod_cache = function() {
  if (_mod_cache == null) {
    _mod_cache = make_cache(locations);
  }
  return _mod_cache;
};

Collections = function(typename) {
  var mod, mod_cache;
  mod_cache = _get_mod_cache();
  if (collection_overrides[typename]) {
    return collection_overrides[typename];
  }
  mod = mod_cache[typename];
  if (mod == null) {
    throw new Error("Module `" + typename + "' does not exists. The problem may be two fold. Either a model was requested that's available in an extra bundle, e.g. a widget, or a custom model was requested, but it wasn't registered before first usage.");
  }
  if (mod.Collection == null) {
    mod.Collection = make_collection(mod.Model);
  }
  return mod.Collection;
};

Collections.register = function(name, collection) {
  return collection_overrides[name] = collection;
};

Collections.register_locations = function(locations, force, errorFn) {
  var cache, mod_cache, module, name, results;
  if (force == null) {
    force = false;
  }
  if (errorFn == null) {
    errorFn = null;
  }
  mod_cache = _get_mod_cache();
  cache = make_cache(locations);
  results = [];
  for (name in cache) {
    if (!hasProp.call(cache, name)) continue;
    module = cache[name];
    if (force || !mod_cache.hasOwnProperty(name)) {
      results.push(mod_cache[name] = module);
    } else {
      results.push(typeof errorFn === "function" ? errorFn(name) : void 0);
    }
  }
  return results;
};

Collections.registered_names = function() {
  return Object.keys(_get_mod_cache());
};

index = {};

module.exports = {
  collection_overrides: collection_overrides,
  locations: locations,
  index: index,
  Collections: Collections,
  Config: Config
};
