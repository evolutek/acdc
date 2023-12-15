#!/bin/bash

function clean() {
    rmdir "$mnt_root_dir"
    rmdir "$mnt_dir"
}

function error() {
    echo "A command failed, exiting"
    clean
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
read -p "Input device (eg. /dev/sda): " src_dev

# src_root_dev="/dev/$src_root_dev_name"
read -p "Input root partition device (eg. /dev/sda2): " src_root_dev

src_root_dev_name="$(basename "$src_root_dev")"
src_dev_name="$(basename "$src_dev")"

GAP_SIZE="64" # In megabytes
DD_BS="$((32 * 1024))" # In bytes

# Create image steps:
# - Delete dphys swapfile from src device
# - Create a file 'gap' full of zero of size GAP on source device
# - Resize root filesystem of src device to minimum size
# - Resize root partition of src device
# - Delete file 'gap' on source device
# - DD to img file through compressor from src device
# - Restore root partition size of src device
# - Restore root filesystem size of src device

title "Creating temporary mount directory"

mnt_dir="$(mktemp -d)"
mnt_root_dir="$mnt_dir/root"

mkdir "$mnt_root_dir" || error
mount $src_root_dev "$mnt_root_dir" || error

# Create gap file and delete swapfile

# Delete swapfile
title "Deleting swapfile"
if [ -f "$mnt_root_dir/etc/dphys-swapfile" ]; then
	swapfile="$(cat "$mnt_root_dir/etc/dphys-swapfile" | grep ^CONF_SWAPFILE | cut -f 2 -d=)"
	if [ "$swapfile" != "" ]; then
        if [ -f "$swapfile" ]; then
            rm "$swapfile" || error
        fi
	fi
fi

# Create gap file
title "Creating gap file"
#gap_filename="$(mktemp -p "$mnt_root_dir" --suffix=-gap)"
gap_filename="$mnt_root_dir/tmp-gap-file"
dd if=/dev/zero of="$gap_filename" bs=1M count=$GAP_SIZE || error

# Shrink filesystem as much as possible
title "Shrinking root filesystem"
umount $src_root_dev || error
e2fsck -p -f $src_root_dev || error
resize2fs -M -p $src_root_dev || error

# Shrink partition

# Get shrinked filesystem size
title "Getting shrinked filesystem size"
mount $src_root_dev "$mnt_root_dir" || error
src_root_df="$(df --block-size=1 --output=source,size "$src_root_dev")"
src_root_size="$(echo "$src_root_df" | tail -n +2 | grep -e "^$src_root_dev" | tr -s ' ' | cut -d ' ' -f 2)"

# Delete gab file
title "Deleting gap file"
rm "$gap_filename" || error

umount $src_root_dev || error

# Delete and recreate root partition

title "Getting root partition information"
src_root_part_size="$(cat /sys/block/$src_dev_name/$src_root_dev_name/size)"
src_root_part_start="$(cat /sys/block/$src_dev_name/$src_root_dev_name/start)"
src_root_part_no="$(cat /sys/block/$src_dev_name/$src_root_dev_name/partition)"

title "Resizing root partition"
sfdisk -b -a -N $src_root_part_no $src_dev <<EOF || error
size=$(((src_root_size + 1023) / 1024))KiB
EOF

# Create image
title "Creating image file"
src_blk_size="$(sudo blockdev --getpbsz "$src_dev")"
src_root_part_new_size="$(cat /sys/block/$src_dev_name/$src_root_dev_name/size)"
src_size_to_cpy=$(((src_root_part_new_size + src_root_part_start) * src_blk_size))
echo "Start copying of $((src_size_to_cpy / 1024 / 1024)) MiB"
dd if=$src_dev status=progress bs=${DD_BS} count=$(((src_size_to_cpy + DD_BS - 1) / DD_BS)) | xz --fast --compress > "$img_filename" || error

# Restore root parititon size
title "Restoring root partition size"
sfdisk -a -N $src_root_part_no $src_dev <<EOF || error
size=$src_root_part_size
EOF

# Restore root filesystem size
title "Restoring root filesystem file"
e2fsck -p -f $src_root_dev || error
resize2fs $src_root_dev || error

# Delete temporary folder
title "Deleting temporary mount folder"
clean
