using System;
using System.Text.RegularExpressions;

public class Example
{
   #line 1 "C:\Users\test"
   public static void Main()
   {
      /****"@"
      ; " @ '"\
      */
      string input = "Not a regex*****";
      string regex = "\\w+_[\\w\"]+_\\w+w";
      /**/
      string pattern = @"x""\d+.\d+.\d+!";
      char c = '"';
      char d = '\"';
      Regex r = new Regex(@"\b(?<word>\w+)\s+x\b", RegexOptions.IgnoreCase);
      Regex r = new Regex(
          "\\b(?<word>\\w+)\\s+\\b",
          // What?
          /**/
          RegexOptions.IgnoreCase
      );
      Something(@"
         (a              # An a
           *   # starred
         )  # bracket
         *  # starred again
      x", x);
   }
}
