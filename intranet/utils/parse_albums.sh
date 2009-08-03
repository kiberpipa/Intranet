#!/usr/bin/env bash
shopt -s extglob
shopt -s nullglob
out="$1"
shift
for i; do 
    i="${i%%/}"
    [[ -f $i/photos.dat ]] && { 
        echo '# -*- coding: utf-8 -*-'
        echo 'from intranet.www.models import Gallery'
        echo 'from photologue.models import Photo'
        echo 'from django.template.defaultfilters import slugify'
        echo 'def unique(item,cls,slug_field,loop=0):'
        echo '  item = item[:40-loop]'
        echo '  if item in [i[slug_field] for i in cls.objects.all().values(slug_field)]:'
        echo '      return unique(item + "_", cls, slug_field, loop=loop+1)'
        echo '  else:'
        echo '    return item'
        IFS=$'\a' read title desc < <( tr -d '\r'  < $i/album.dat | sed ':b;$!N; $!bb; $s/\n/\\\\\\\\n/g' | ssed -nR 's/.*?s:5:"title".*?"(.*?)".*?s:11:"description".*?"(.*?)";.*/\1'$'\a'\\2/p)
        title=${title//\'/\\\\\\\'}
        albums=`tr -d '\r' < "$i"/photos.dat | sed -rn 's/s:11:"isAlbumName";s:8:"([^"]*)"/\n\t\1\n/gp' | sed '/\t/!d'`
        printf "try:\n    gallery = Gallery.objects.get(album_name='${i%/}')\nexcept Gallery.DoesNotExist:\n    gallery = Gallery.objects.create(title=unique(u'$title', Gallery, 'title'), title_slug=unique(slugify(u'$title'), Gallery, 'title_slug'), description=u'$desc', album_name='${i%/}')\n"
        for album in $albums; do
            IFS=$'\a' read subtitle subdesc < <( tr -d '\r'  < $album/album.dat | sed ':b;$!N; $!bb; $s/\n/\\\\\\\\n/g' | ssed -nR 's/.*?s:5:"title".*?"(.*?)".*?s:11:"description".*?"(.*?)";.*/\1'$'\a'\\2/p)
            subdesc=`echo -n "$subdesc" | sed ':b; $!N; $!bb; $s/\\n/\\\\\\\\n/g'`
            subtitle=${subtitle//\'/\\\\\\\'}
            printf "try:\n    child = Gallery.objects.get(album_name='$album')\n    child.parent = gallery\n    child.save()\nexcept Gallery.DoesNotExist:\n    child = Gallery.objects.create(title=unique(u'$subtitle', Gallery, 'title'), title_slug=unique(slugify(u'$subtitle'), Gallery, 'title_slug'), parent=gallery, description=u'%s', album_name='$album')\n" "$subdesc"
        done

        for j in $i/!(*.thumb|*.sized|*.highlight).@(jpg|jpeg|png|gif); do
            dirless=${j##*/}
            title=${dirless%.*}
            c=`tr -d '\r' < "$i"/photos.dat | sed ':b; $!N; $!bb; $s/\n/\\\\\\\\n/g' | ssed -nR 's/.*?"'"$title"'".*?caption";s:[0-9]+:"(.*?)";.*/\1\n/p'`
            caption="${c//\'/\\\'}"
            if [[ $caption != $title && $caption ]]; then cap=", caption=u'$caption'"; fi
            printf "p=Photo.objects.create(title_slug=unique(slugify(u'$j'), Photo, 'title_slug'),title=unique(u'$j', Photo, 'title'),image='$j'$cap)\np.save()\ngallery.photos.add(p)\n"
        done
    } | iconv -f latin1 -t utf8 | sed -e 's//ž/g' -e 's//š/g' -e 's/è/č/g' -e 's/¹/š/g' > "$out/${i%/}".py
done 

for i in */album.dat; do
    echo '# -*- coding: utf-8 -*-'
    echo 'from intranet.www.models import Gallery'
    parent=`tr -d '\r' < $i | tr -d '\n' | ssed -R 's/.*parentAlbumName.*?:"(.*?)".*/\1/'` 
    me="${i%/*}"
    if [[ $parent == 'clicks' ]]; then
        printf "me = Gallery.objects.get(album_name='$me')\nme.parent = None\nme.save()\n"
    else
        printf "me = Gallery.objects.get(album_name='$me')\nme.parent = Gallery.objects.get(album_name='$parent')\nme.save()\n"
    fi
done > "$out/zzzzz-relations.py"
