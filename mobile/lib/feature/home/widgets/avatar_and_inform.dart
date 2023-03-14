import 'package:flutter/material.dart';
import 'package:license_plate_detect/core/theme/app_data.dart';

class AvatarandInform extends StatelessWidget {
  final String? imagePath;
  final VoidCallback onClicked;

  const AvatarandInform({
    Key? key,
    required this.imagePath,
    required this.onClicked,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        InkWell(
          onTap: onClicked,
          child: Container(
              padding: const EdgeInsets.all(4),
              decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(12),
                  color: Colors.grey[200],
                  ),
              child: ClipOval(
                child:
                imagePath != null ?
                Image.network(
                  imagePath!,
                  height: 32,
                  width: 32,
                  fit: BoxFit.fill,
                ) :  Image.asset(
                  "assets/avata_default.jpg",
                  height: 32,
                  width: 32,
                  fit: BoxFit.fill,
                )
              )),
        ),
        Container(
            padding: EdgeInsets.all(4),
            decoration: BoxDecoration(
              color: Colors.grey[200],
              borderRadius: BorderRadius.circular(12),
            ),
            child: Image.asset(
              AppData.icBell,
              height: 32,
              width: 32,
              fit: BoxFit.fill,
            ))
      ],
    );
  }
}
