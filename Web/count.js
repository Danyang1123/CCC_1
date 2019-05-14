/*------------------------------------------------------------
 * Program: count.js
 * Purpuose: The mapper function of a CouchDB view, which is
 *           to be used together built-in reducer _count to
 *           count number of tweets per location.
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
    emit(doc.location, 1);
}
