#!/bin/bash

function error() {
    echo "A command failed, exiting"
    exit 1
}

function title() {
    echo ""
    echo "======== $1 ========"
    echo ""
    #read -p "Press enter to continue ..." dummy
}

#img_filename="acdc.img.xz"
read -p "Output filename: " img_filename

#src_dev="/dev/"
read -p "Output device (eg. /dev/sda): " dst_dev

DD_BS="$((32 * 1024))" # In bytes

# Write image steps:
# - Check if dst size > img size + gap
# - DD to dst device through compressor from img file
# - Resize root parition of dst device to maximum size
# - Resize root filesystem of dst device
# - Change dst disk to a new random id (and label if desired)

title "Writing image to disk"

xz --stdout --decompress "$img_filename" | dd of=$dst_dev status=progress bs=$DD_BS || error
lsblk

# title "Writing new random disk id"
# new_id=$(od -A n -t x -N 4 /dev/urandom | tr -d " ")
# sfdisk --disk-id $dst_dev 0x$new_id || error

title "Getting root partition information"

root_part_dev="$(sfdisk $dst_dev -l | grep -e "^$dst_dev" | tail -n 1 | tr -s ' ' | cut -d ' ' -f 1)"
root_part_no="$(basename $root_part_dev | tr -dc '0-9')"
echo "root_part_no: $root_part_no"

title "Resizing root partition"

parted $dst_dev resizepart $root_part_no 100% || error

title "Resizing root filesystem"

e2fsck -p -f $root_part_dev || error
resize2fs $root_part_dev || error
