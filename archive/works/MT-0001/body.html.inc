     <p>My bibliography lists a 1994 print edition of Bruce Lincoln’s <cite>Authority: Construction and Corrosion</cite>.
      Searching OpenAlex turned up the same author, title and year. That seemed enough until I checked the identifiers.
      My record gave a print ISBN. The candidate’s DOI identified an electronic edition.
      I could trace both records to Lincoln’s book, but I had no independent evidence that the edition in the database corresponded to the one on my list.
      I left the edition unresolved and excluded it from the citation sample.
      <a href="https://openalex.org/W4229660601">Lincoln’s OpenAlex record</a></p>
     <p>For Joseph Henrich’s 2009 paper on costly displays, the database title omitted the subtitle in my bibliography.
      The author, main title and DOI agreed, so I accepted the match and used the article’s OpenAlex reference list.
      The longer title mattered less here than the edition did for Lincoln.
      <a href="https://openalex.org/W2128261329">Henrich’s OpenAlex record</a></p>
     <h2>Following one citation through a conversion</h2>
     <p>Henrich’s paper and a later paper by Ara Norenzayan and colleagues shared two cited works in a small excerpt of their OpenAlex records.
      That gives four citation links to follow, two from each article.
      One shared reference has the identifier <code>W621128614</code>.</p>
     <p>In the bibliometrix 5.5.0 workflow I tested, the OpenAlex importer shortened reference URLs to bare IDs.
      When the software built the network, it kept only reference strings longer than ten characters.
      <code>W621128614</code> has exactly ten. Applying that rule to the excerpt drops one link from each paper.
      The papers now appear to share only one of the two references. Both articles are still present.</p>
     <p>I now record the reason for accepting a work or edition before comparing its citation links across formats.
      The first decision needs bibliographic evidence. For the second, I can compare the document and reference IDs row by row.
      The public example includes the four source links, the filtered result and a version in which all four links survive.
      <a href="https://github.com/raylee-ai/bibliographic-metadata-audit">Run the offline citation audit</a></p>
