/*------------------------------------------------------------
 * Program: sum.js
 * Purpuose: The mapper function of a CouchDB view, which is
 *           to be used together built-in reducer _sum to get
 *           the sums of each factor (sentiment + 7 sins) of
 *           grouped by location.
 *
 * Group Member:
 *          Victor Ding 1000272
 *          Zhuolin He 965346
 *          Chenyao Wang 928359
 *          Danyang Wang 963747
 *          Yuming Zhang 973693
 *------------------------------------------------------------*/

function (doc)
{
    var keywords = ["sentiment", "pride", "greed", "lust", "envy", "gluttony", "wrath", "sloth"];
    var result = {};
    keywords.forEach(function (keyword)
    {
        result[keyword] = doc[keyword];
    });
    emit(doc.location, result);
}
