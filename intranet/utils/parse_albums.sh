#!/usr/bin/env bash
shopt -s extglob
shopt -s nullglob
for i in */; do 
#for i in Aktivizem/; do 
    [[ -f $i/photos.dat ]] && { 
        echo '# -*- coding: utf-8 -*-' 
        echo 'from intranet.photologue.models import Gallery, Photo'
        echo 'from django.template.defaultfilters import slugify'
        cat /tmp/t.py
        IFS=$'\a' read title desc < <( tr -d '\r'  < $i/album.dat | sed ':b;$!N; $!bb; $s/\n/\\\\\\\\n/g' | ssed -nR 's/.*?s:5:"title".*?"(.*?)".*?s:11:"description".*?"(.*?)";.*/\1'$'\a'\\2/p)
        title=${title//\'/\\\\\\\'}
        albums=`tr -d '\r' < "$i"/photos.dat | sed -rn 's/s:11:"isAlbumName";s:8:"([^"]*)"/\n\t\1\n/gp' | sed '/\t/!d'`
        printf "try:\n    gallery = Gallery.objects.get(album_name='${i%/}')\nexcept Gallery.DoesNotExist:\n    gallery = Gallery.objects.create(title=unique(u'$title', 'title'), title_slug=unique(slugify(u'$title'), 'title_slug'), description=u'$desc', album_name='${i%/}')\n"
        for album in $albums; do
            IFS=$'\a' read subtitle subdesc < <( tr -d '\r'  < $album/album.dat | sed ':b;$!N; $!bb; $s/\n/\\\\\\\\n/g' | ssed -nR 's/.*?s:5:"title".*?"(.*?)".*?s:11:"description".*?"(.*?)";.*/\1'$'\a'\\2/p)
            subdesc=`echo -n "$subdesc" | sed ':b; $!N; $!bb; $s/\\n/\\\\\\\\n/g'`
            subtitle=${subtitle//\'/\\\\\\\'}
            printf "try:\n    child = Gallery.objects.get(album_name='$album')\n    child.parent = gallery\n    child.save()\nexcept Gallery.DoesNotExist:\n    child = Gallery.objects.create(title=unique(u'$subtitle', 'title'), title_slug=unique(slugify(u'$subtitle'), 'title_slug'), parent=gallery, description=u'%s', album_name='$album')\n" "$subdesc"
        done

        for j in $i/!(*.thumb|*.sized|*.highlight).@(jpg|jpeg|png|gif); do
            dirless=${j##*/}
            title=${dirless%.*}
            c=`tr -d '\r' < "$i"/photos.dat | sed ':b; $!N; $!bb; $s/\n/\\\\\\\\n/g' | ssed -nR 's/.*?"'"$title"'".*?caption";s:[0-9]+:"(.*?)";.*/\1\n/p'`
            caption="${c//\'/\\\'}"
            if [[ $caption != $title && $caption ]]; then cap=", caption=u'$caption'"; fi
            printf "p=Photo.objects.create(image='$j'$cap)\np.save()\ngallery.photos.add(p)\n"
        done
    } | iconv -f latin2 -t utf8 > "/home/intranet/gallery_migrate/6/${i%/}"
done 
