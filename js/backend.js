/*global require: false, module: false */
'use strict';

var Rx = require('rx');
require('rx-dom');
var _ = require('underscore');
var qs = require('qs');

// XXX Need a config mechanism for this.
//var databaseUrl = "http://brcaexchange.cloudapp.net/backend";
var databaseUrl = "http://localhost:8000";

var transpose = a => _.zip.apply(_, a);

// URIs have a 2083 character size limit and some search terms exceed that.
// Limit the length and cut at a semicolon if possible to ensure the search works
function trimSearchTerm(search) {
    var maxLength = 200;
    if (search.length > maxLength) {
        search = search.slice(0, maxLength);
        var lastColonPosition = search.lastIndexOf(":");
        if (lastColonPosition !== -1) {
            search = search.slice(0, lastColonPosition);
        }
    }
    return search;
}

// XXX these defaults might produce odd user experience, since they
// are not reflected in the UI.
function url(opts) {
    var {
        format = 'json',
        filterValues = {},
        sortBy: {prop = 'Gene_Symbol', order = 'ascending'} = {},
        pageLength = 100,
        page = 0,
        search = '',
        column,
        include,
        exclude
        } = opts,

        [filter, filterValue] = transpose(_.pairs(_.pick(filterValues, v => v)));
    search = trimSearchTerm(search);

    return `${databaseUrl}/data/?${qs.stringify(_.pick({
        format,
        filter,
        filterValue,
        'order_by': prop,
        direction: order,
        'page_size': pageLength,
        'page_num': page,
        'search_term': search,
        'column': column,
        'include': include,
        'exclude': exclude
    }, v => v != null), {arrayFormat: 'repeat'})}`;
}

function data(opts) {
    return Rx.DOM.get(url(opts)).map(xhr => JSON.parse(xhr.responseText));
}

function lollipopData(opts) {
    opts.pageLength = 0;
    opts.format = 'json';
    opts.column = ['id', 'Genomic_Coordinate_hg38', 'Pathogenicity_default'];
    return Rx.DOM.get(url(opts)).map(xhr => JSON.parse(xhr.responseText));
}

module.exports = {
    data,
    lollipopData,
    url,
    trimSearchTerm,
    databaseUrl
};
