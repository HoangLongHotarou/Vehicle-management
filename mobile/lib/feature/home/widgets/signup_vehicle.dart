import 'package:flutter/material.dart';
import 'package:license_plate_detect/core/theme/app_color.dart';

class SignunVehicle extends StatelessWidget {
  
  final VoidCallback onClicked;
  
  const SignunVehicle({
    Key? key,
    required this.onClicked
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 100,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(15),
          color: AppColor.primaryColor),
      child: Row(
        children: [
          Expanded(
              flex: 4,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Text(
                    'Đăng ký xe!',
                    style: Theme.of(context).textTheme.titleLarge!.copyWith(
                          color: AppColor.white,
                        ),
                  ),
                  Text(
                      'Đăng ký để sử dụng hệ thống nhận diện biển số xe tự động',
                      style: Theme.of(context).textTheme.titleSmall!.copyWith(
                            color: AppColor.white,
                          ))
                ],
              )),
          Expanded(
              flex: 2,
              child: InkWell(
                onTap: onClicked,
                child: Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(15),
                      color: AppColor.white),
                  child: Text('Đăng ký',
                      textAlign: TextAlign.center,
                      style: Theme.of(context).textTheme.titleLarge!.copyWith(color: AppColor.primaryColor)),
                ),
              )),
        ],
      ),
    );
  }
}
