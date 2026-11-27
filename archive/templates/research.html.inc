<section aria-labelledby="research-title" class="index-head">
  <h1 id="research-title">Research</h1>
  <p>Browse the archive by type, field and first publication date.</p>
</section>
<form id="filters" class="filters" aria-label="Filter research" hidden>
  <label>Work type<select name="type"><option value="">All types</option>$types</select></label>
  <label>Research field<select name="area"><option value="">All fields</option>$areas</select></label>
  <label>Published from<input type="date" name="from"></label>
  <label>Through<input type="date" name="to"></label>
  <button type="reset">Clear filters</button>
</form>
<section aria-labelledby="entries-heading" class="writings index-list">
  <h2 id="entries-heading" class="sr-only">Archive entries</h2>
  <p id="result-count" class="result-count" role="status" aria-live="polite" aria-atomic="true">$count</p>
$entries
  <p id="empty" hidden>No work matches these filters.</p>
</section>
