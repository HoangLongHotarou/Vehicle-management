// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:license_plate_detect/core/component/build_button.dart';
import 'package:license_plate_detect/core/theme/app_data.dart';

import '../../../core/theme/app_color.dart';
import '../../home/presention/HomePage.dart';
import '../../../services/auth/auth.dart';
import '../../login/presention/LoginPage.dart';
import '../../personalinfomation/presention/PersonalInfomationPage.dart';
import '../widgets/button_setting.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  int _selectedIndex = 2;

  void _onItemTapped(int index) {
    if (index == 0) {
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) {
        return MyHomePage();
      }));
    }

    if (index == 1) {
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) {
        return PersonalInfomationPage();
      }));
    }
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text(
            "Cài đặt",
            textAlign: TextAlign.start,
            style: Theme.of(context).textTheme.headlineMedium!,
          ),
        backgroundColor: Colors.transparent,
        leadingWidth: 0,
        elevation: 0,
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home_outlined),
            label: 'Trang chủ',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.info_outline),
            label: 'Thông tin',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: 'Cài đặt',
          ),
        ],
        currentIndex: _selectedIndex,
        unselectedItemColor: Colors.grey,
        selectedItemColor: AppColor.primaryColor,
        onTap: _onItemTapped,
      ),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal:24),
        child: ListView(
          // mainAxisAlignment: MainAxisAlignment.start,
          // crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Text(
            //   'Cài đặt',
            //   style: Theme.of(context).textTheme.headlineMedium,
            // ),
            // SizedBox(
            //   height: 12,
            // ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Chung',
                  style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: AppColor.primaryColor),
                ),
                SizedBox(
                  height: 12,
                ),
                buttonSetting(
                  icon: Icons.language_outlined,
                  title: 'Ngôn ngữ',
                  onClicked: () {
                    print('logout');
                  },
                ),
                buttonSetting(
                  icon: Icons.light_mode,
                  title: 'Chế độ sáng/tối',
                  onClicked: () {
                    print('logout');
                  },
                ),
                buttonSetting(
                  icon: Icons.logout_outlined,
                  title: 'Đăng xuất',
                  onClicked: () async {
                    await Authenticate.logout();
                    Navigator.push(context,
                        MaterialPageRoute(builder: (context) {
                      return LoginPage();
                    }));
                  },
                ),
                buttonSetting(
                  icon: Icons.delete_outline,
                  title: 'Xóa tài khoản',
                  onClicked: () {
                    print('logout');
                  },
                ),
              ],
            ),
            SizedBox(
              height: 12,
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Phản hồi',
                  style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: AppColor.primaryColor),
                ),
                SizedBox(
                  height: 12,
                ),
                buttonSetting(
                  icon: Icons.warning_amber_outlined,
                  title: 'Báo cáo lỗi',
                  onClicked: () {
                    print('logout');
                  },
                ),
                buttonSetting(
                  icon: Icons.feedback_outlined,
                  title: 'Gửi phản hồi',
                  onClicked: () {
                    print('logout');
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
