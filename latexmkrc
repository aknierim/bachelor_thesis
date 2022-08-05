$cleanup_mode = 1;
$out_dir = "build";
$pdflatex = "lualatex -interaction=nonstopmode -halt-on-error %O %S";
$pdf_mode = 1;
@default_files = ("thesis.tex");
add_cus_dep( 'glo', 'gls', 0, 'makeglossaries' );
sub makeglossaries {
   $dir = dirname($_[0]);
   $file = basename($_[0]);
   system( "makeglossaries", "-d", $dir, $file );
}

push @generated_exts, "bcf bbl";
$clean_ext = "bcf bbl glg glo gls run.xml xdy"
